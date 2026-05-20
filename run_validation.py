import subprocess
import os

print("🚀 Running LangGraph Agent Validation Suite on Actual Data...")
print("=" * 60)

# Run the validation report generator
try:
    print("📋 Generating Validation Report...")
    # Fix the import issues in generate_report by running it with PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = "/Users/charanb/Desktop/TGL_Customised/final_ui/pytests:" + env.get("PYTHONPATH", "")
    subprocess.run(["python3", "pytests/generate_report.py"], env=env, check=True)
    print("✅ Report generated: pytests/validation_report.md")
except Exception as e:
    print(f"❌ Error generating report: {e}")

# Read and display the report
if os.path.exists("pytests/validation_report.md"):
    with open("pytests/validation_report.md", "r") as f:
        print("\n" + "=" * 60)
        print("📊 VALIDATION RESULTS")
        print("=" * 60)
        print(f.read())
else:
    print("❌ Validation report file not found.")
