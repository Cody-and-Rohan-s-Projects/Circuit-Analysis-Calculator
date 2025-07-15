package com.codyandrohan.circuitanalyzer

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import kotlin.math.*
import org.apache.commons.math3.complex.Complex
import org.apache.commons.math3.linear.*

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            CircuitAnalyzerApp()
        }
    }
}

@Composable
fun CircuitAnalyzerApp() {
    var equationCount by remember { mutableStateOf(3) }
    var precision by remember { mutableStateOf(2) }
    val clipboardManager = LocalClipboardManager.current
    val context = LocalContext.current

    var matrix by remember { mutableStateOf(Array(4) { Array(4) { "" } }) }
    var vector by remember { mutableStateOf(Array(4) { "" }) }

    var output by remember { mutableStateOf("Enter values and click Solve.") }
    var isDarkTheme by remember { mutableStateOf(true) }

    MaterialTheme(colors = if (isDarkTheme) darkColors() else lightColors()) {
        Column(
            modifier = Modifier
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            Text("Circuit Analysis Calculator", style = MaterialTheme.typography.h5)
            Spacer(Modifier.height(8.dp))
            Button(onClick = {
                val githubIntent = Intent(Intent.ACTION_VIEW, Uri.parse("https://github.com/Cody-and-Rohan-s-Projects/Circuit-Analyser"))
                context.startActivity(githubIntent)
            }) {
                Text("View on GitHub")
            }

            Row {
                Text("Equations:")
                Spacer(Modifier.width(8.dp))
                DropdownMenu(equationCount, (1..4).toList(), onValueChange = { equationCount = it })
            }

            Row {
                Text("Precision:")
                Spacer(Modifier.width(8.dp))
                DropdownMenu(precision, (0..6).toList(), onValueChange = { precision = it })
            }

            Spacer(Modifier.height(12.dp))
            MatrixInput(matrix, vector, equationCount) { m, v ->
                matrix = m
                vector = v
            }

            Spacer(Modifier.height(8.dp))

            Button(onClick = {
                try {
                    output = solveCircuit(matrix, vector, equationCount, precision)
                } catch (e: Exception) {
                    output = "Error: ${e.message}"
                }
            }) {
                Text("Solve")
            }

            Button(onClick = {
                clipboardManager.setText(androidx.compose.ui.text.AnnotatedString(output))
                output += "\n\nCopied to clipboard."
            }) {
                Text("Copy Result")
            }

            Button(onClick = {
                isDarkTheme = !isDarkTheme
            }) {
                Text("Toggle Theme")
            }

            Spacer(Modifier.height(16.dp))
            Text(output)
        }
    }
}

@Composable
fun MatrixInput(
    matrix: Array<Array<String>>,
    vector: Array<String>,
    size: Int,
    onChange: (Array<Array<String>>, Array<String>) -> Unit
) {
    val newMatrix = matrix.map { it.copyOf() }.toTypedArray()
    val newVector = vector.copyOf()

    for (i in 0 until size) {
        Row(Modifier.padding(vertical = 4.dp)) {
            for (j in 0 until size) {
                OutlinedTextField(
                    value = newMatrix[i][j],
                    onValueChange = {
                        newMatrix[i][j] = it
                        onChange(newMatrix, newVector)
                    },
                    modifier = Modifier.width(70.dp),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Text),
                    placeholder = { Text("A${i+1}${j+1}") }
                )
            }

            Spacer(Modifier.width(8.dp))

            OutlinedTextField(
                value = newVector[i],
                onValueChange = {
                    newVector[i] = it
                    onChange(newMatrix, newVector)
                },
                modifier = Modifier.width(70.dp),
                singleLine = true,
                placeholder = { Text("b${i+1}") }
            )
        }
    }
}

fun solveCircuit(
    matrix: Array<Array<String>>,
    vector: Array<String>,
    size: Int,
    precision: Int
): String {
    val A = Array2DRowFieldMatrix<Complex>(ComplexField.getInstance(), size, size)
    val b = ArrayFieldVector<Complex>(ComplexField.getInstance(), size)

    for (i in 0 until size) {
        for (j in 0 until size) {
            A.setEntry(i, j, parseComplex(matrix[i][j]))
        }
        b.setEntry(i, parseComplex(vector[i]))
    }

    val solver = FieldLUDecomposition(A).solver
    if (!solver.isNonSingular) {
        return "Error: Singular matrix or invalid inputs."
    }

    val x = solver.solve(b)

    val resultLines = (0 until size).map {
        val value = x.getEntry(it)
        val angle = Math.toDegrees(value.argument)
        val magnitude = value.abs()
        "I${it + 1} = ${formatComplex(value, precision)} A   [ $magnitude ∠ $angle° A ]"
    }

    val kvlLines = (0 until size).map { i ->
        val terms = (0 until size).mapNotNull { j ->
            val coeff = A.getEntry(i, j)
            if (!coeff.equals(Complex.ZERO)) {
                "${formatComplex(coeff, precision)} Ω * I${j + 1}"
            } else null
        }
        val rhs = b.getEntry(i)
        "${terms.joinToString(" + ")} = ${formatComplex(rhs, precision)} V"
    }

    return "Solution:\n${resultLines.joinToString("\n")}\n\nKVL Equations:\n${kvlLines.joinToString("\n")}"
}

fun parseComplex(input: String): Complex {
    val cleaned = input.trim().lowercase().replace("i", "j").replace(" ", "")
    return Complex(cleaned)
}

fun formatComplex(c: Complex, precision: Int): String {
    val real = "%.${precision}f".format(c.real)
    val imag = "%.${precision}f".format(c.imaginary)
    return "$real + ${imag}j"
}

@Composable
fun <T> DropdownMenu(selected: T, options: List<T>, onValueChange: (T) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    Box {
        Button(onClick = { expanded = true }) {
            Text("$selected")
        }
        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            options.forEach {
                DropdownMenuItem(onClick = {
                    onValueChange(it)
                    expanded = false
                }) {
                    Text("$it")
                }
            }
        }
    }
}
