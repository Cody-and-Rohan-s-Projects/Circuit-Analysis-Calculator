// CircuitAnalysisActivity.kt
package com.codyandrohan.circuit_analyser

import android.os.Bundle
import android.text.InputType
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class CircuitAnalysisActivity : AppCompatActivity() {

    private lateinit var matrixContainer: LinearLayout
    private lateinit var vectorContainer: LinearLayout
    private lateinit var resultLabel: TextView
    private lateinit var kvlLabel: TextView
    private lateinit var matrixSizeSpinner: Spinner
    private lateinit var solveButton: Button
    private lateinit var resetButton: Button
    private lateinit var linkBox: TextView
    private var matrixSize = 3

    data class Complex(val re: Double, val im: Double) {
        operator fun plus(c: Complex) = Complex(re + c.re, im + c.im)
        operator fun minus(c: Complex) = Complex(re - c.re, im - c.im)
        operator fun times(c: Complex) = Complex(re * c.re - im * c.im, re * c.im + im * c.re)
        operator fun div(c: Complex): Complex {
            val denom = c.re * c.re + c.im * c.im
            return Complex((re * c.re + im * c.im) / denom, (im * c.re - re * c.im) / denom)
        }

        override fun toString(): String {
            val sign = if (im >= 0) "+" else "-"
            return "%.3f%s%.3fj".format(re, sign, kotlin.math.abs(im))
        }
    }

    private fun parseComplex(input: String): Complex {
        val s = input.trim().lowercase().replace("i", "j")

        val fullPattern = Regex("""^([+-]?\d*\.?\d+)?([+-]?\d*\.?\d*)j$""")

        return try {
            when {
                // Real + Imaginary (-7+j5 or 3-4j)
                fullPattern.matches(s) -> {
                    val match = fullPattern.find(s)!!
                    val (realPart, imagPartRaw) = match.destructured

                    val real = if (realPart.isBlank()) 0.0 else realPart.toDouble()
                    val imag = when (imagPartRaw) {
                        "+", "" -> 1.0
                        "-" -> -1.0
                        else -> imagPartRaw.toDouble()
                    }

                    Complex(real, imag)
                }

                // Pure imaginary like j5, -j2.3
                Regex("""^[+-]?j\d*\.?\d+$""").matches(s) -> {
                    val imag = s.replace("j", "").toDouble()
                    Complex(0.0, imag)
                }

                // j or -j
                Regex("""^[+-]?j$""").matches(s) -> {
                    val imag = if (s.startsWith("-")) -1.0 else 1.0
                    Complex(0.0, imag)
                }

                // real only
                else -> Complex(s.toDouble(), 0.0)
            }
        } catch (e: Exception) {
            throw IllegalArgumentException("Invalid complex number format: '$input'")
        }
    }


    private fun solveLinearSystemComplex(
        a: Array<Array<Complex>>,
        b: Array<Complex>
    ): Array<Complex>? {
        val n = a.size
        val A = a.map { it.copyOf() }.toTypedArray()
        val B = b.copyOf()

        for (i in 0 until n) {
            var maxRow = i
            for (k in i + 1 until n) {
                val mag1 = A[k][i].re * A[k][i].re + A[k][i].im * A[k][i].im
                val mag2 = A[maxRow][i].re * A[maxRow][i].re + A[maxRow][i].im * A[maxRow][i].im
                if (mag1 > mag2) maxRow = k
            }
            if (A[maxRow][i].re == 0.0 && A[maxRow][i].im == 0.0) return null

            val tmpA = A[i]; A[i] = A[maxRow]; A[maxRow] = tmpA
            val tmpB = B[i]; B[i] = B[maxRow]; B[maxRow] = tmpB

            for (k in i + 1 until n) {
                val factor = A[k][i] / A[i][i]
                for (j in i until n) A[k][j] = A[k][j] - factor * A[i][j]
                B[k] = B[k] - factor * B[i]
            }
        }

        val x = Array(n) { Complex(0.0, 0.0) }
        for (i in n - 1 downTo 0) {
            var sum = B[i]
            for (j in i + 1 until n) sum -= A[i][j] * x[j]
            x[i] = sum / A[i][i]
        }
        return x
    }

    private fun buildMatrixInputs(size: Int) {
        matrixContainer.removeAllViews()
        vectorContainer.removeAllViews()

        for (i in 0 until size) {
            // ----------- MATRIX ROW -----------
            val matrixRow = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
            }

            // Left bracket
            val leftBracket = TextView(this).apply {
                text = when (i) {
                    0 -> "⎡"
                    size - 1 -> "⎣"
                    else -> "⎢"
                }
                textSize = 24f
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply { setMargins(4, 4, 4, 4) }
            }

            matrixRow.addView(leftBracket)

            // Matrix input fields
            for (j in 0 until size) {
                val input = EditText(this).apply {
                    hint = "A${i + 1}${j + 1}"
                    inputType = InputType.TYPE_CLASS_TEXT
                    layoutParams =
                        LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)
                            .apply {
                                setMargins(4, 4, 4, 4)
                            }
                }
                matrixRow.addView(input)
            }

            // Right bracket
            val rightBracket = TextView(this).apply {
                text = when (i) {
                    0 -> "⎤"
                    size - 1 -> "⎦"
                    else -> "⎥"
                }
                textSize = 24f
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply { setMargins(4, 4, 4, 4) }
            }

            matrixRow.addView(rightBracket)
            matrixContainer.addView(matrixRow)

            // ----------- VECTOR ROW -----------
            val vectorRow = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
            }

            // Left bracket for vector
            val vectorLeftBracket = TextView(this).apply {
                text = when (i) {
                    0 -> "⎡"
                    size - 1 -> "⎣"
                    else -> "⎢"
                }
                textSize = 24f
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply { setMargins(4, 4, 4, 4) }
            }

            // Vector input
            val bInput = EditText(this).apply {
                hint = "b${i + 1}"
                inputType = InputType.TYPE_CLASS_TEXT
                layoutParams = LinearLayout.LayoutParams(
                    0,
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    1f
                ).apply {
                    setMargins(4, 4, 4, 4)
                }
            }

            // Right bracket for vector
            val vectorRightBracket = TextView(this).apply {
                text = when (i) {
                    0 -> "⎤"
                    size - 1 -> "⎦"
                    else -> "⎥"
                }
                textSize = 24f
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply { setMargins(4, 4, 4, 4) }
            }

            vectorRow.addView(vectorLeftBracket)
            vectorRow.addView(bInput)
            vectorRow.addView(vectorRightBracket)

            vectorContainer.addView(vectorRow)
        }
    }

    private fun solveSystem() {
        try {
            val n = matrixSize
            val A = Array(n) { Array(n) { Complex(0.0, 0.0) } }
            val b = Array(n) { Complex(0.0, 0.0) }

            // Parse matrix A
            for (i in 0 until n) {
                val row = matrixContainer.getChildAt(i) as LinearLayout
                // Skip index 0 (left bracket), read EditTexts from index 1 to n
                for (j in 0 until n) {
                    val valText = (row.getChildAt(j + 1) as EditText).text.toString()
                    A[i][j] = if (valText.isBlank()) Complex(0.0, 0.0) else parseComplex(valText)
                }
            }

            // Parse vector b
            for (i in 0 until n) {
                val vectorRow = vectorContainer.getChildAt(i) as LinearLayout
                // Index 1 is the EditText (bracketed layout: [TextView, EditText, TextView])
                val valText = (vectorRow.getChildAt(1) as EditText).text.toString()
                b[i] = if (valText.isBlank()) Complex(0.0, 0.0) else parseComplex(valText)
            }

            // Solve system
            val x = solveLinearSystemComplex(A, b)
            if (x == null) {
                resultLabel.text = "Error: Singular matrix — no solution."
                kvlLabel.text = ""
                return
            }

            // Display solution
            resultLabel.text = buildString {
                append("Solution:\n")
                for (i in x.indices) append("I${i + 1} = ${x[i]} A\n")
            }.trim()

            // Display KVL equations
            kvlLabel.text = buildString {
                append("KVL Equations:\n")
                for (i in 0 until n) {
                    val row = mutableListOf<String>()
                    for (j in 0 until n) {
                        val coeff = A[i][j]
                        if (coeff.re != 0.0 || coeff.im != 0.0) {
                            val formatted = coeff.toString().removePrefix("+")
                            val sign =
                                if (row.isEmpty()) "" else if (formatted.startsWith("-")) "- " else "+ "
                            row.add("$sign${formatted.trimStart('-')}·I${j + 1}")
                        }
                    }
                    row.add("= ${b[i]} V")
                    append(row.joinToString(" "))
                    append("\n")
                }
            }.trim()

        } catch (e: Exception) {
            resultLabel.text = "Error: ${e.message ?: "Invalid input"}"
            kvlLabel.text = ""
        }
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        matrixContainer = findViewById(R.id.matrix_container)
        vectorContainer = findViewById(R.id.vector_container)
        resultLabel = findViewById(R.id.result_label)
        kvlLabel = findViewById(R.id.kvl_label)
        matrixSizeSpinner = findViewById(R.id.size_spinner)
        solveButton = findViewById(R.id.solve_button)
        resetButton = findViewById(R.id.reset_button)
        linkBox = findViewById(R.id.info_link)

        resultLabel.setTextIsSelectable(true)
        kvlLabel.setTextIsSelectable(true)

        linkBox.text = "View on GitHub"
        linkBox.setOnClickListener {
            val url = "https://github.com/Cody-and-Rohan-s-Projects/Circuit-Analyser/tree/Android"
            val intent = android.content.Intent(android.content.Intent.ACTION_VIEW)
            intent.data = android.net.Uri.parse(url)
            startActivity(intent)
        }


        val sizes = (1..4).map { it.toString() }
        matrixSizeSpinner.adapter =
            ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, sizes)
        matrixSizeSpinner.setSelection(2)
        matrixSizeSpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>,
                view: View?,
                position: Int,
                id: Long
            ) {
                matrixSize = sizes[position].toInt()
                buildMatrixInputs(matrixSize)
            }

            override fun onNothingSelected(parent: AdapterView<*>) {}
        }

        solveButton.setOnClickListener { solveSystem() }
        resetButton.setOnClickListener {
            buildMatrixInputs(matrixSize)
            resultLabel.text = getString(R.string.results_will_appear)
            kvlLabel.text = getString(R.string.kvl_equations)
        }

        buildMatrixInputs(matrixSize)
    }
}
