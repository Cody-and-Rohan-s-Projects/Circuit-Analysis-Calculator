package com.codyandrohan.circuit_analyser

import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.appcompat.widget.SwitchCompat

class MainActivity : AppCompatActivity() {

    private lateinit var themeSwitch: SwitchCompat
    private lateinit var sizeSpinner: Spinner
    private lateinit var setSizeButton: Button
    private lateinit var matrixContainer: LinearLayout
    private lateinit var vectorContainer: LinearLayout
    private lateinit var solveButton: Button
    private lateinit var resultLabel: TextView
    private lateinit var kvlLabel: TextView

    private var matrixSize = 2  // default 2x2 system

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Bind views
        themeSwitch = findViewById(R.id.theme_switch)
        sizeSpinner = findViewById(R.id.size_spinner)
        setSizeButton = findViewById(R.id.set_size_button)
        matrixContainer = findViewById(R.id.matrix_container)
        vectorContainer = findViewById(R.id.vector_container)
        solveButton = findViewById(R.id.solve_button)
        resultLabel = findViewById(R.id.result_label)
        kvlLabel = findViewById(R.id.kvl_label)

        // Setup spinner
        val spinnerItems = (2..5).map { "$it x $it" }
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, spinnerItems)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        sizeSpinner.adapter = adapter

        sizeSpinner.setSelection(0)

        // Toggle dark/light theme
        themeSwitch.setOnCheckedChangeListener { _, isChecked ->
            AppCompatDelegate.setDefaultNightMode(
                if (isChecked)
                    AppCompatDelegate.MODE_NIGHT_YES
                else
                    AppCompatDelegate.MODE_NIGHT_NO
            )
        }

        // Set matrix/vector input size
        setSizeButton.setOnClickListener {
            matrixSize = sizeSpinner.selectedItemPosition + 2
            buildMatrixInputs(matrixSize)
        }

        // Solve system
        solveButton.setOnClickListener {
            solveSystem()
        }

        // Build initial 2x2 matrix
        buildMatrixInputs(matrixSize)
    }

    private fun buildMatrixInputs(size: Int) {
        matrixContainer.removeAllViews()
        vectorContainer.removeAllViews()

        for (i in 0 until size) {
            val rowLayout = LinearLayout(this)
            rowLayout.orientation = LinearLayout.HORIZONTAL

            for (j in 0 until size) {
                val input = EditText(this).apply {
                    hint = "A${i + 1}${j + 1}"
                    layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)
                    inputType = android.text.InputType.TYPE_CLASS_NUMBER or android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL
                }
                rowLayout.addView(input)
            }

            matrixContainer.addView(rowLayout)

            val bInput = EditText(this).apply {
                hint = "B${i + 1}"
                layoutParams = LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT)
                inputType = android.text.InputType.TYPE_CLASS_NUMBER or android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL
            }
            vectorContainer.addView(bInput)
        }
    }

    private fun solveSystem() {
        try {
            val aMatrix = Array(matrixSize) { DoubleArray(matrixSize) }
            val bVector = DoubleArray(matrixSize)

            // Collect A matrix values
            for (i in 0 until matrixSize) {
                val row = matrixContainer.getChildAt(i) as LinearLayout
                for (j in 0 until matrixSize) {
                    val input = row.getChildAt(j) as EditText
                    aMatrix[i][j] = input.text.toString().toDoubleOrNull() ?: 0.0
                }
            }

            // Collect B vector values
            for (i in 0 until matrixSize) {
                val input = vectorContainer.getChildAt(i) as EditText
                bVector[i] = input.text.toString().toDoubleOrNull() ?: 0.0
            }

            // Solve using basic Gaussian elimination
            val result = solveLinearSystem(aMatrix, bVector)

            resultLabel.text = getString(R.string.solution_result, result.joinToString(", "))
            kvlLabel.text = getString(R.string.kvl_equations)

        } catch (_: Exception) {
            resultLabel.text = getString(R.string.results_will_appear)
        }
    }

    private fun solveLinearSystem(a: Array<DoubleArray>, b: DoubleArray): DoubleArray {
        val n = a.size
        val x = DoubleArray(n)

        // Forward elimination
        for (i in 0 until n) {
            var maxRow = i
            for (k in i + 1 until n) {
                if (Math.abs(a[k][i]) > Math.abs(a[maxRow][i])) {
                    maxRow = k
                }
            }

            val tmpA = a[i]
            a[i] = a[maxRow]
            a[maxRow] = tmpA

            val tmpB = b[i]
            b[i] = b[maxRow]
            b[maxRow] = tmpB

            for (k in i + 1 until n) {
                val factor = a[k][i] / a[i][i]
                for (j in i until n) {
                    a[k][j] -= factor * a[i][j]
                }
                b[k] -= factor * b[i]
            }
        }

        // Back substitution
        for (i in n - 1 downTo 0) {
            var sum = b[i]
            for (j in i + 1 until n) {
                sum -= a[i][j] * x[j]
            }
            x[i] = sum / a[i][i]
        }

        return x
    }
}
