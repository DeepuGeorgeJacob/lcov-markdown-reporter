# 📖 LCOV to Markdown Pure Action

**Convert LCOV code coverage reports into clean, readable Markdown tables and append them directly to your GitHub Job Summary.**

## ✨ Features

This action is a lightweight, pure **Python** utility packaged as a Docker Action. It integrates code coverage into your CI/CD pipeline without relying on external web services.

* **Simple Output:** Generates a Markdown table summarizing line and function coverage metrics per file.

* **Job Summary Integration:** Appends the generated report directly to the **GitHub Job Summary** using `$GITHUB_STEP_SUMMARY`.

* **Zero Dependencies:** The Python script uses only the standard library, eliminating installation failures.

* **Containerized:** Runs in a minimal Docker container for a consistent environment.

## 🚀 Usage

To use this action, your previous workflow step must generate an **LCOV (`.info`) file** (e.g., from Jest, Flutter, or your testing framework).

### Basic Example Workflow (`.github/workflows/coverage.yml`)

This example demonstrates generating the report, displaying it in the Job Summary, and uploading the raw Markdown file as an artifact.

```yaml
name: CI & Coverage Report

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build_and_report:
    runs-on: ubuntu-latest
    steps:
      - name: ⬇️ Checkout code
        uses: actions/checkout@v4

      # 1. Run Tests and Generate LCOV File (MUST be done first)
      - name: ⚙️ Run Tests (Example Node/Jest)
        run: |
          npm install
          # Replace 'coverage/lcov.info' if your path is different
          npm test -- --coverage --coverageReporters=lcov

      # 2. Convert LCOV to Markdown using this Action
      - name: 📝 Generate Markdown Report
        uses: DeepuGeorgeJacob/lcov-markdown-reporter@v1 
        id: lcov_report
        with:
          lcov-file: coverage/lcov.info
          output-file: coverage_report.md

      # 3. Display the Markdown report in the Job Summary
      # The 'cat' command reads the file created by the previous step and appends it to the summary
      - name: 📊 Append Report to Job Summary
        run: cat coverage_report.md >> $GITHUB_STEP_SUMMARY

      # 4. Optional: Save the raw Markdown file as a permanent artifact
      - name: 📦 Upload Coverage Report Artifact
        uses: actions/upload-artifact@v4
        with:
          name: coverage-markdown-report
          path: coverage_report.md
          retention-days: 7
```
## 📤 Outputs

This action writes the report directly to the runner's shared disk. The `output-file` name is provided as a step output for other steps (like the `cat` command or `upload-artifact`) to reference the file path.

| Name | Description | 
| :--- | :--- | 
| **`output-file`** | The filename of the generated markdown file on the runner (e.g., `coverage_report.md`). | 

## 📜 License

This project is licensed under the **[MIT License]**.

## 🙏 Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/[USER/REPO]/issues).