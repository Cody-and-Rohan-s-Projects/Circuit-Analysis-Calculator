package com.codyandrohan.circuit_analyser

import android.os.Bundle
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class CircuitAnalysisActivity : AppCompatActivity() {

    private lateinit var matrixContainer: LinearLayout
    private lateinit var vectorContainer: LinearLayout
    private lateinit var resultLabel: TextView
    private lateinit var kvlLabel: TextView
    private lateinit var matrixSizeSpinner: Spinner
    private lateinit var decimalSpinner: Spinner
    private lateinit var solveButton: Button
    private lateinit var resetButton: Button
    private lateinit var linkBox: TextView
    private var matrixSize = 3
    private var decimalPlaces = 3

    data class Complex(val re: Double, val im: Double) {
        operator fun plus(c: Complex) = Complex(re + c.re, im + c.im)
        operator fun minus(c: Complex) = Complex(re - c.re, im - c.im)
        operator fun times(c: Complex) = Complex(re * c.re - im * c.im, re * c.im + im * c.re)
        operator fun div(c: Complex): Complex {
            val denom = c.re * c.re + c.im * c.im
            return Complex((re * c.re + im * c.im) / denom, (im * c.re - re * c.im) / denom)
        }

        fun toFormattedString(precision: Int): String {
            val sign = if (im >= 0) "+" else "-"
            val formatStr = "%.${precision}f"
            return "${formatStr.format(re)}$sign${formatStr.format(kotlin.math.abs(im))}j"
        }

        override fun toString(): String {
            // fallback default formatting if needed
            return toFormattedString(3)
        }
    }

    // Polar conversion with dynamic precision
    private fun rectangularToPolar(c: Complex, precision: Int): String {
        val magnitude = kotlin.math.hypot(c.re, c.im)
        val angle = Math.toDegrees(kotlin.math.atan2(c.im, c.re))
        val formatStr = "%.${precision}f"
        return "${formatStr.format(magnitude)} ∠ ${formatStr.format(angle)}°"
    }

    private fun parseComplex(input: String): Complex {
        val cleaned = input
            .lowercase()
            .replace("i", "j")
            .replace(",", "")
            .replace(" ", "")

        if (cleaned == "j") return Complex(0.0, 1.0)
        if (cleaned == "-j") return Complex(0.0, -1.0)
        if (cleaned == "+j") return Complex(0.0, 1.0)

        // General complex number pattern:
        val pattern = Regex("""^([+-]?\d*\.?\d+)?([+-]?(?:j\d*\.?\d+|\d*\.?\d+j|j))?$""")
        val match = pattern.matchEntire(cleaned)
            ?: throw IllegalArgumentException("Invalid complex number format: '$input'")

        val (realRaw, imagRaw) = match.destructured

        val real = if (realRaw.isBlank()) 0.0 else realRaw.toDouble()

        val imag = when {
            imagRaw.isBlank() -> 0.0
            imagRaw == "j" || imagRaw == "+j" -> 1.0
            imagRaw == "-j" -> -1.0
            imagRaw.startsWith("+j") -> imagRaw.removePrefix("+j").toDouble()
            imagRaw.startsWith("-j") -> -imagRaw.removePrefix("-j").toDouble()
            imagRaw.startsWith("j") -> imagRaw.removePrefix("j").toDouble()
            imagRaw.endsWith("j") -> imagRaw.removeSuffix("j").toDouble()
            else -> throw IllegalArgumentException("Invalid imaginary part: '$imagRaw'")
        }

        return Complex(real, imag)
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
            val matrixRow = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
            }
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

            for (j in 0 until size) {
                val input = EditText(this).apply {
                    hint = "A${i + 1}${j + 1}"
                    gravity = Gravity.CENTER
                    inputType = InputType.TYPE_CLASS_TEXT
                    layoutParams =
                        LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)
                            .apply { setMargins(4, 4, 4, 4) }
                }
                matrixRow.addView(input)
            }

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

            val vectorRow = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
            }
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
            val bInput = EditText(this).apply {
                hint = "b${i + 1}"
                gravity = Gravity.CENTER
                inputType = InputType.TYPE_CLASS_TEXT
                layoutParams = LinearLayout.LayoutParams(
                    0,
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    1f
                ).apply { setMargins(4, 4, 4, 4) }
            }
            val vectorRightBracket = TextView(this).apply {
                text = when (i) {
                    0 -> "⎤"
                    size - 1 -> "⎦"
                    else -> "⎥"
                }
                textSize = 24f
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT,
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

            for (i in 0 until n) {
                val row = matrixContainer.getChildAt(i) as LinearLayout
                for (j in 0 until n) {
                    val valText = (row.getChildAt(j + 1) as EditText).text.toString()
                    A[i][j] = if (valText.isBlank()) Complex(0.0, 0.0) else parseComplex(valText)
                }
            }

            for (i in 0 until n) {
                val vectorRow = vectorContainer.getChildAt(i) as LinearLayout
                val valText = (vectorRow.getChildAt(1) as EditText).text.toString()
                b[i] = if (valText.isBlank()) Complex(0.0, 0.0) else parseComplex(valText)
            }

            val x = solveLinearSystemComplex(A, b)
            if (x == null) {
                resultLabel.text = "Error: Singular matrix — no solution."
                kvlLabel.text = ""
                return
            }

            resultLabel.text = buildString {
                append("Solution:\n\n")
                for (i in x.indices) {
                    append("I${i + 1} = ${x[i].toFormattedString(decimalPlaces)} A\n")
                    append("    [${rectangularToPolar(x[i], decimalPlaces)} A]\n")
                }
            }.trim()

            kvlLabel.text = buildString {
                append("KVL Equations:\n\n")
                for (i in 0 until n) {
                    val row = mutableListOf<String>()
                    for (j in 0 until n) {
                        val coeff = A[i][j]
                        if (coeff.re != 0.0 || coeff.im != 0.0) {
                            val formatted = coeff.toFormattedString(decimalPlaces).removePrefix("+")
                            val sign =
                                if (row.isEmpty()) "" else if (formatted.startsWith("-")) "- " else "+ "
                            row.add("$sign(${formatted.trimStart('-')})*I${j + 1}")
                        }
                    }
                    row.add("= ${b[i].toFormattedString(decimalPlaces)} V\n")
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
        decimalSpinner = findViewById(R.id.decimal_spinner)
        solveButton = findViewById(R.id.solve_button)
        resetButton = findViewById(R.id.reset_button)
        linkBox = findViewById(R.id.info_link)

        resultLabel.setTextIsSelectable(true)
        kvlLabel.setTextIsSelectable(true)

        linkBox.setOnClickListener {
            val url = "https://github.com/Cody-and-Rohan-s-Projects/Circuit-Analyser"
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
                parent: AdapterView<*>, view: View?, position: Int, id: Long
            ) {
                matrixSize = sizes[position].toInt()
                buildMatrixInputs(matrixSize)
            }

            override fun onNothingSelected(parent: AdapterView<*>) {}
        }

        // Setup decimal places spinner
        val precisionOptions = (1..6).map { it.toString() }
        decimalSpinner.adapter =
            ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, precisionOptions)
        decimalSpinner.setSelection(2) // default to 3 decimal places
        decimalSpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>, view: View?, position: Int, id: Long
            ) {
                decimalPlaces = precisionOptions[position].toInt()
                // Optional: re-solve to update displayed results with new precision
                // solveSystem()
            }

            override fun onNothingSelected(parent: AdapterView<*>) {}
        }

        solveButton.setOnClickListener { solveSystem() }
        resetButton.setOnClickListener {
            buildMatrixInputs(matrixSize)
            resultLabel.text = getString(R.string.results_will_appear)
            kvlLabel.text = getString(R.string.kvl_equations)
        }

        val clipboardButton = findViewById<Button>(R.id.clipboard_button)
        clipboardButton.setOnClickListener {
            val resultText = resultLabel.text.toString()
            val kvlText = kvlLabel.text.toString()
            val combinedText = "$resultText\n\n$kvlText"

            val clipboard = getSystemService(CLIPBOARD_SERVICE) as android.content.ClipboardManager
            val clip = android.content.ClipData.newPlainText("Circuit Solution", combinedText)
            clipboard.setPrimaryClip(clip)

            Toast.makeText(this, "Copied to clipboard", Toast.LENGTH_SHORT).show()
        }

        buildMatrixInputs(matrixSize)
    }
}
