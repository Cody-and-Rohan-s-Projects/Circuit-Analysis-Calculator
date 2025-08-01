//
//  ContentView.swift
//  Circuit Analyser
//
//  Created by Cody on 7/15/25
//  Updated: 7/31/25
//
//  Description:
//  This file defines the main user interface for the Circuit Analyser app,
//  allowing users to input matrix and vector data to solve electrical circuits.
//
//  Author: Cody Carter and Rohan Patel
//  Editor: Cody Carter

import SwiftUI

// Extension to allow custom hex colors for UI
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int = UInt64()
        Scanner(string: hex).scanHexInt64(&int)
        
        let r, g, b, a: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (r, g, b, a) = (
                (int >> 8) * 17,
                (int >> 4 & 0xF) * 17,
                (int & 0xF) * 17,
                255
            )
        case 6: // RGB (24-bit)
            (r, g, b, a) = (
                int >> 16,
                int >> 8 & 0xFF,
                int & 0xFF,
                255
            )
        case 8: // ARGB (32-bit)
            (r, g, b, a) = (
                int >> 16 & 0xFF,
                int >> 8 & 0xFF,
                int & 0xFF,
                int >> 24
            )
        default:
            (r, g, b, a) = (0, 0, 0, 255)
        }
        
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

// Adds custom colors and attributes to matrix text boxes
struct ColoredPlaceholderTextField: View {
    let placeholder: String
    @Binding var text: String
    let isDarkMode: Bool
    let placeholderColor: Color
    let width: CGFloat
    var textAlignment: TextAlignment = .center

    var body: some View {
        TextField(
            "",
            text: $text,
            prompt: Text(placeholder)
                .foregroundColor(placeholderColor)
        )
        .multilineTextAlignment(textAlignment)
        .padding(8)
        .frame(width: width)
        .foregroundColor(isDarkMode ? Color.white : Color.black)
        .overlay(
            Rectangle()
                .frame(height: 2)
                .foregroundColor(text.isEmpty
                                 ? (isDarkMode ? Color.white.opacity(0.6) : Color.gray)
                                 : (isDarkMode ? Color.gray : Color.gray)),
            alignment: .bottom
        )
    }
}


// Parses and cleans inputed strings into a useable format to be calculated
// Includes operator cases to apply arithmetic to the complex number type struct
struct Complex {
    var real: Double
    var imag: Double
    
    func toFormattedString(_ precision: Int) -> String {
        let fmt = "%.\(precision)f"
        let sign = imag >= 0 ? "+" : "-"
        return "\(String(format: fmt, real)) \(sign) \(String(format: fmt, abs(imag)))j"
    }
    
    init(_ real: Double, _ imag: Double) {
        self.real = real
        self.imag = imag
    }
    
    init(from string: String) {
        let cleaned = string.replacingOccurrences(of: " ", with: "").lowercased()

        // Handle special case: pure imaginary "j", "+j", "-j"
        if cleaned == "j" {
            self.real = 0
            self.imag = 1
            return
        } else if cleaned == "-j" {
            self.real = 0
            self.imag = -1
            return
        } else if cleaned == "+j" {
            self.real = 0
            self.imag = 1
            return
        }

        // Handle pure imaginary: "4j", "-3.2j"
        let pureImagPattern = #"^([-+]?\d*\.?\d*)j$"#
        if let match = cleaned.range(of: pureImagPattern, options: .regularExpression) {
            let imagStr = String(cleaned[match]).dropLast() // remove 'j'
            self.real = 0
            self.imag = Double(imagStr) ?? 0
            return
        }

        // Handle full complex: "3+4j", "-2.5-6j"
        let complexPattern = #"^([-+]?\d*\.?\d*)([-+]\d*\.?\d*)j$"#
        let regex = try! NSRegularExpression(pattern: complexPattern)
        if let match = regex.firstMatch(in: cleaned, range: NSRange(cleaned.startIndex..., in: cleaned)) {
            let realRange = Range(match.range(at: 1), in: cleaned)
            let imagRange = Range(match.range(at: 2), in: cleaned)
            let realStr = realRange.map { String(cleaned[$0]) } ?? "0"
            let imagStr = imagRange.map { String(cleaned[$0]) } ?? "0"
            self.real = Double(realStr) ?? 0
            self.imag = Double(imagStr) ?? 0
            return
        }

        // Handle real only
        self.real = Double(cleaned) ?? 0
        self.imag = 0
    }
    
    static func /(lhs: Complex, rhs: Complex) -> Complex {
        let denom = rhs.real * rhs.real + rhs.imag * rhs.imag
        return Complex(
            (lhs.real * rhs.real + lhs.imag * rhs.imag) / denom,
            (lhs.imag * rhs.real - lhs.real * rhs.imag) / denom
        )
    }
    
    static func -(lhs: Complex, rhs: Complex) -> Complex {
        Complex(lhs.real - rhs.real, lhs.imag - rhs.imag)
    }
    
    static func *(lhs: Complex, rhs: Complex) -> Complex {
        Complex(
            lhs.real * rhs.real - lhs.imag * rhs.imag,
            lhs.imag * rhs.real + lhs.real * rhs.imag
        )
    }
    
    static func +(lhs: Complex, rhs: Complex) -> Complex {
        Complex(lhs.real + rhs.real, lhs.imag + rhs.imag)
    }

    static prefix func -(value: Complex) -> Complex {
        Complex(-value.real, -value.imag)
    }

    static func ==(lhs: Complex, rhs: Complex) -> Bool {
        abs(lhs.real - rhs.real) < 1e-9 && abs(lhs.imag - rhs.imag) < 1e-9
    }

    func conjugate() -> Complex {
        Complex(real, -imag)
    }
    
    var magnitude: Double {
        sqrt(real * real + imag * imag)
    }

    var angleDegrees: Double {
        atan2(imag, real) * 180 / .pi
    }

    func toPolarString(_ precision: Int) -> String {
        let fmt = "%.\(precision)f"
        return "\(String(format: fmt, magnitude)) ∠ \(String(format: fmt, angleDegrees))°"
    }
}

// UI and widget placement logic
struct ContentView: View {
    @State private var precision = 2
    @State private var matrixSize = 3
    @State private var matrix: [[String]] = Array(repeating: Array(repeating: "", count: 3), count: 3)
    @State private var vector: [String] = Array(repeating: "", count: 3)
    @State private var results: [String] = []
    @State private var showSolution = false
    @State private var isDarkMode = false
    @State private var solutionText: String = ""
    
    
    var body: some View {
        ScrollView {
            VStack(spacing: 4) {
                Text("Circuit Analysis Calculator")
                    .font(.title) // or .system(size: 28)
                    .bold()
                    .foregroundColor(.blue) // Built-in SwiftUI color
                
                Text("by Cody Carter and Rohan Patel")
                    .font(.subheadline) // or .system(size: 16)
                    .foregroundColor(.gray)
                
                Link(destination: URL(string: "https://github.com/Cody-and-Rohan-s-Projects/Circuit-Analyser")!) {
                    Text("View our GitHub!")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundColor(.white)
                        .padding(.horizontal, 24)
                        .padding(.vertical, 12)
                        .background(
                            RoundedRectangle(cornerRadius: 8)
                                .fill(Color.gray)
                        )
                        .overlay(
                            RoundedRectangle(cornerRadius: 8)
                                .stroke(Color.gray, lineWidth: 2)
                        )
                }
                .buttonStyle(PlainButtonStyle())
                
                HStack(spacing: 8) {
                    Text("Dark Mode")
                        .font(.body)
                    Toggle("", isOn: $isDarkMode)
                        .labelsHidden()
                }
                .padding()
            }
            
            HStack(spacing: 16) {
                Text("Number of Equations:")
                    .foregroundColor(isDarkMode ? .white : .black)
                Picker("", selection: $matrixSize) {
                    ForEach(1...4, id: \.self) { Text("\($0)")}
                }
                .tint(.white)
                .foregroundColor(.white)
                .frame(width: 60)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(Color.teal, lineWidth: 2)
                )
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.teal) // Fill color
                )
                .pickerStyle(.menu)
            }
            
            HStack() {
                Text("Decimal Precision:")
                    .foregroundColor(isDarkMode ? .white : .black)
                Picker("", selection: $precision) {
                    ForEach(1...6, id: \.self) { Text("\($0)") }
                }
                .tint(.white)
                .foregroundColor(.white)
                .frame(width: 60)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(Color.teal, lineWidth: 2)
                )
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.teal) // Fill color
                )
                .pickerStyle(.menu)
            }
            
            
            VStack(spacing: 16) {
                Button("Confirm Matrix Size") {
                    matrix = Array(repeating: Array(repeating: "", count: matrixSize), count: matrixSize)
                    vector = Array(repeating: "", count: matrixSize)
                    results = []
                    showSolution = false
                }
                .padding(.horizontal, 24) // wider side padding
                .padding(.vertical, 12)   // taller button
                .foregroundColor(.white)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(Color.blue, lineWidth: 2)
                )
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.blue) // Fill color
                )
                Spacer()
                    .frame(height: 24)
            }
            
            
            VStack{
                if vector.count == matrixSize {
                    Text("Coefficient Matrix [A]:")
                        .foregroundColor(isDarkMode ? .white : .black)
                        .bold()
                    HStack(alignment: .top, spacing: 4) {
                        VStack(alignment: .leading, spacing: 4) {
                            if matrixSize == 1 {
                                HStack(spacing: 4) {
                                    Text("[")
                                        .font(.title)
                                        .padding(.top, 2)
                                        .padding(.bottom, 6)
                                    ColoredPlaceholderTextField(
                                        placeholder: "A11",
                                        text: $matrix[0][0],
                                        isDarkMode: isDarkMode,
                                        placeholderColor: isDarkMode ? Color(hex: "#E0E0E0") : Color(hex: "#BDBDBD"),
                                        width: 80
                                    )
                                    Text("]")
                                        .font(.title)
                                        .padding(.top, 2)
                                        .padding(.bottom, 6)
                                }
                            }
                            else {
                                ForEach(0..<matrixSize, id: \.self) { i in
                                    HStack(spacing: 4) {
                                        // Leading bracket
                                        Text(i == 0 ? "⎡" : i == matrixSize - 1 ? "⎣" : "⎢")
                                            .font(.title)
                                            .padding(.top, i == 0 ? 0 : i == matrixSize - 1 ? 8 : 4)
                                        
                                            .padding(.bottom, i == 0 ? 8 : i == matrixSize - 1 ? 0 : 4)
                                        
                                        ForEach(0..<matrixSize, id: \.self) { j in
                                            ColoredPlaceholderTextField(
                                                placeholder: "A\(i+1)\(j+1)",
                                                text: $matrix[i][j],
                                                isDarkMode: isDarkMode,
                                                placeholderColor: isDarkMode ? Color(hex: "#E0E0E0") : Color(hex: "#BDBDBD"),
                                                width: 80
                                            )
                                        }
                                        
                                        // Trailing bracket
                                        Text(i == 0 ? "⎤" : i == matrixSize - 1 ? "⎦" : "⎥")
                                            .font(.title)
                                            .padding(.top, i == 0 ? 0 : i == matrixSize - 1 ? 8 : 4)
                                        
                                            .padding(.bottom, i == 0 ? 8 : i == matrixSize - 1 ? 0 : 4)
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            VStack {
                if vector.count == matrixSize {
                    Text("Constants Vector [b]:")
                        .foregroundColor(isDarkMode ? .white : .black)
                        .bold()
                    VStack(alignment: .leading, spacing: 4) {
                        if matrixSize == 1 {
                            HStack(spacing: 4) {
                                Text("[")
                                    .font(.title)
                                    .padding(.top, 2)
                                    .padding(.bottom, 6)
                                ColoredPlaceholderTextField(
                                    placeholder: "B1",
                                    text: $vector[0],
                                    isDarkMode: isDarkMode,
                                    placeholderColor: isDarkMode ? Color(hex: "#E0E0E0") : Color(hex: "#BDBDBD"),
                                    width: 80
                                )
                                Text("]")
                                    .font(.title)
                                    .padding(.top, 2)
                                    .padding(.bottom, 6)
                            }
                        }
                        else {
                            ForEach(0..<matrixSize, id: \.self) { i in
                                HStack(spacing: 4) {
                                    // Left bracket
                                    Text(i == 0 ? "⎡" : i == matrixSize - 1 ? "⎣" : "⎢")
                                        .font(.title)
                                        .padding(.top, i == 0 ? 0 : i == matrixSize - 1 ? 8 : 4)
                                    
                                        .padding(.bottom, i == 0 ? 8 : i == matrixSize - 1 ? 0 : 4)
                                    
                                    ColoredPlaceholderTextField(
                                        placeholder: "B\(i+1)",
                                        text: $vector[i],
                                        isDarkMode: isDarkMode,
                                        placeholderColor: isDarkMode ? Color(hex: "#E0E0E0") : Color(hex: "#BDBDBD"),
                                        width: 80
                                    )
                                    
                                    
                                    // Right bracket
                                    Text(i == 0 ? "⎤" : i == matrixSize - 1 ? "⎦" : "⎥")
                                        .font(.title)
                                        .padding(.top, i == 0 ? 0 : i == matrixSize - 1 ? 8 : 4)
                                    
                                        .padding(.bottom, i == 0 ? 8 : i == matrixSize - 1 ? 0 : 4)
                                }
                            }
                        }
                    }
                }
            }
            
            
            VStack(alignment: .center, spacing: 16) {
                HStack(spacing: 16) {
                    Button("Solve") {
                        let result = solveSystem(matrix: matrix, vector: vector)
                        solutionText = "Solution:\n \(result)"
                        showSolution = true
                    }
                    .padding(.horizontal, 24)
                    .padding(.vertical, 12)
                    .foregroundColor(.white)
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(Color(hex: "#66BB6A"))
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color(hex: "#66BB6A"), lineWidth: 2)
                    )
                    
                    Button("Copy Solution") {
                        UIPasteboard.general.string = solutionText
                    }
                    
                    .padding(.horizontal, 24)
                    .padding(.vertical, 12)
                    .foregroundColor(.white)
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(Color(hex: "#42A5F5"))
                    )
                    
                    Button("Clear") {
                        matrix = Array(repeating: Array(repeating: "", count: matrixSize), count: matrixSize)
                        vector = Array(repeating: "", count: matrixSize)
                        results = []
                        solutionText = ""
                        showSolution = false
                    }
                    .padding(.horizontal, 24)
                    .padding(.vertical, 12)
                    .foregroundColor(.white)
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(Color(hex: "#EF5350"))
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color(hex: "#EF5350"), lineWidth: 2)
                    )
                    
                    
                }
                
                if !showSolution{
                    Text("Enter values and then tap Solve. The result and equations will appear here.")
                        .foregroundColor(isDarkMode ? .white : .black)
                        .bold()
                }
                
                if showSolution {
                    ScrollView {
                        Text(solutionText)
                            .font(.system(.body, design: .monospaced))
                            .foregroundColor(isDarkMode ? .white : .black)
                            .padding()
                    }
                    .frame(maxHeight: 300)
                }
            }
            .padding()
            .preferredColorScheme(isDarkMode ? .dark : .light)
        }
    }
    
    // Backend to solve the cleaned matrix using Cramers rule
    func solveSystem(matrix: [[String]], vector: [String]) -> String {
        let originalA = matrix.map { row in row.map { Complex(from: $0) } }
        let originalB = vector.map { Complex(from: $0) }
        
        var A = matrix.map { row in row.map { Complex(from: $0) }}
        var b = vector.map { Complex(from: $0) }
        let n = matrixSize
        
        guard matrix.count == matrixSize,
              vector.count == matrixSize,
              matrix.allSatisfy({ $0.count == matrixSize }) else {
            return "Error: Invalid matrix size or shape"
        }
        
        for i in 0..<n {
            let pivot = A[i][i]
            
            let tolerance = 1e-10
            if abs(pivot.real) < tolerance && abs(pivot.imag) < tolerance {
                results = ["Error: Confirm matrix size"]
                return "Error"
            }
            
            for j in i..<n {
                A[i][j] = A[i][j] / pivot
            }
            b[i] = b[i] / pivot
            
            for k in 0..<n {
                if k != i {
                    let factor = A[k][i]
                    for j in i..<n {
                        A[k][j] = A[k][j] - factor * A[i][j]
                    }
                    b[k] = b[k] - factor * b[i]
                }
            }
        }
        
        // Rectangular and polar conversion in solution box
        let fmt = "%.\(precision)f"
        results = b.enumerated().map { i, val in
            let real = val.real
            let imag = val.imag
            let magnitude = sqrt(real * real + imag * imag)
            let angleRad = atan2(imag, real)
            let angleDeg = angleRad * 180 / .pi
            let rect = "\(String(format: fmt, real)) + \(String(format: fmt, imag))j"
            let polar = "\(String(format: fmt, magnitude)) ∠ \(String(format: fmt, angleDeg))°"
            return "I\(i+1) = \(rect) (\(polar))"
        }
        
        // Build KVL equations using originalA and originalB in solution box
        var kvlEquations = "KVL Equations:\n"
        for i in 0..<n {
            var terms: [String] = []
            for j in 0..<n {
                let coeff = originalA[i][j]
                if abs(coeff.real) > 1e-10 || abs(coeff.imag) > 1e-10 {
                    let coeffStr = coeff.toFormattedString(precision)
                    let sign = (terms.isEmpty) ? "" : (coeffStr.starts(with: "-") ? "- " : "+ ")
                    let cleanedCoeff = coeffStr.trimmingCharacters(in: CharacterSet(charactersIn: "+- "))
                    terms.append("\(sign)(\(cleanedCoeff)Ω)*I\(j+1)")
                }
            }
            let bStr = originalB[i].toFormattedString(precision)
            terms.append("= \(bStr)")
            kvlEquations += terms.joined(separator: " ") + "\n\n"
        }
        
        showSolution = true
        return results.joined(separator: "\n\n") + "\n\n" + kvlEquations
    }
}
