//
//  ContentView.swift
//  Circuit Analyser
//
//  Created by Penny on 7/16/25.
//

import SwiftUI

struct Complex {
    var real: Double
    var imag: Double
    
    init(_ real: Double, _ imag: Double) {
        self.real = real
        self.imag = imag
    }
    
    init(from string: String) {
        let cleaned = string.replacingOccurrences(of: " ", with: "").lowercased()
        let pattern = #"([-+]?\d*\.?\d*)([-+]\d*\.?\d*)?j"#
        let regex = try! NSRegularExpression(pattern: pattern)
        if let match = regex.firstMatch(in: cleaned, range: NSRange(cleaned.startIndex..., in: cleaned)) {
            let realPart = Double(
                Range(match.range(at: 1), in: cleaned).map { String(cleaned[$0]) } ?? "0"
            ) ?? 0
            let imagPart = Double(
                Range(match.range(at: 2), in: cleaned).map { String(cleaned[$0]) } ?? "1"
            ) ?? 1
            
            self.real = realPart
            self.imag = imagPart
        }
        
        else if cleaned.contains("j") {
            self.real = 0
            self.imag = Double(cleaned.replacingOccurrences(of: "j", with: "")) ?? 1
        }
        
        else {
            self.real = Double(cleaned) ?? 0
            self.imag = 0
        }
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
            lhs.imag * rhs.real - lhs.real * rhs.imag
        )
    }
}

struct ContentView: View {
    @State private var precision = 2
    @State private var matrixSize = 3
    @State private var matrix: [[String]] = Array(repeating: Array(repeating: "", count: 3), count: 3)
    @State private var vector: [String] = Array(repeating: "", count: 3)
    @State private var results: [String] = []
    @State private var showSolution = false
    @State private var isDarkMode = false

    var body: some View {
        ScrollView {
            VStack(spacing: 4) {
                Text("Circuit Analysis Calculator")
                    .font(.title) // or .system(size: 28)
                    .foregroundColor(.blue) // Built-in SwiftUI color

                Text("By Cody Carter and Rohan Patel")
                    .font(.subheadline) // or .system(size: 16)
                    .foregroundColor(.gray)
                
                Link(destination: URL(string: "https://github.com/Cody-and-Rohan-s-Projects/Circuit-Analyser")!) {
                    HStack {
                        Text("View our GitHub")
                    }
                    .foregroundColor(.blue)
                    .font(.system(size: 16, weight: .medium))
                    .padding(8)
                }
                
                HStack(spacing: 8) {
                    Text("Dark Mode")
                        .font(.body)
                    Toggle("", isOn: $isDarkMode)
                        .labelsHidden()
                }
                .padding()
            }
            
            
            HStack(spacing: 16) {
                Text("Decimal Precision:")
                        .foregroundColor(isDarkMode ? .white : .black)
                Picker("", selection: $precision) {
                    ForEach(1...6, id: \.self) { Text("\($0)") }
                }
                .tint(.white)
                .foregroundColor(.white)
                .frame(width: 80)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(Color.blue, lineWidth: 2)
                )
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.blue) // Fill color
                )
                .pickerStyle(.menu)
            }
            
            HStack {
                Text("Number of Equations:")
                    .foregroundColor(isDarkMode ? .white : .black)
                Picker("", selection: $matrixSize) {
                    ForEach(1...4, id: \.self) { Text("\($0)")}
                }
                .tint(.white)
                .foregroundColor(.white)
                .frame(width: 80)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(Color.blue, lineWidth: 2)
                )
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.blue) // Fill color
                )
                .pickerStyle(.menu)
            }
            
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
            
            if vector.count == matrixSize {
                HStack(alignment: .top, spacing: 4) {
                    

                    VStack(alignment: .leading, spacing: 4) {
                        ForEach(0..<matrixSize, id: \.self) { i in
                            HStack(spacing: 4) {
                                // Left bracket
                                Text("[")
                                    .font(.largeTitle)
                                    .padding(.bottom, 6)
                                ForEach(0..<matrixSize, id: \.self) { j in
                                    TextField("A\(i+1)\(j+1)", text: $matrix[i][j])
                                        .textFieldStyle(.roundedBorder)
                                        .frame(width: 60)
                                }
                                // Left bracket
                                Text("]")
                                    .font(.largeTitle)
                                    .padding(.bottom, 6)
                            }
                        }
                    }
                }
            }
            
            if vector.count == matrixSize {
                VStack(alignment: .leading, spacing: 4) {
                    ForEach(0..<matrixSize, id: \.self) { i in
                        HStack(spacing: 4) {
                            Text("[")
                                .font(.title)
                                .padding(.bottom, 6)
                            TextField("b\(i+1)", text: $vector[i])
                                .textFieldStyle(.roundedBorder)
                                .frame(width: 100)
                            Text("]")
                                .font(.title)
                                .padding(.bottom, 6)
                        }
                    }
                }
            }
            
            VStack (spacing: 8){
                Button("Solve") {
                    solveSystem()
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
                
                Button("Clear") {
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
                
                if showSolution {
                    Text("Solution")
                        .font(.headline)
                        .foregroundColor(.black)
                    
                    VStack(alignment: .leading, spacing: 6) {
                        ForEach(results, id: \.self) {
                            Text("\($0) A")
                                .font(.system(.body, design: .monospaced))
                        }
                    }
                    .padding(1)
                }
            }
        } .preferredColorScheme(isDarkMode ? .dark : .light)
    }
    
    
    
    func solveSystem() {
        var A = matrix.map { row in row.map { Complex(from: $0)}}
        var b = vector.map { Complex(from: $0)}
        let n = matrixSize
        
        for i in 0..<n {
            let pivot = A[i][i]
            
            let tolerance = 1e-10
            if abs(pivot.real) < tolerance && abs(pivot.imag) < tolerance {
                results = ["Error: Pivot too close to zero at row \(i+1)."]
                return
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
        
        let fmt = "%.\(precision)f"
        results = b.enumerated().map { i, val in
            "I\(i+1) = \(String(format: fmt, val.real)) + \(String(format: fmt, val.imag))j"
        }
        showSolution = true
    }
}
