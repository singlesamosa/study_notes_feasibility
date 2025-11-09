#!/usr/bin/env python3
"""
Run tests and update the dashboard with results.
"""
import subprocess
import xml.etree.ElementTree as ET
import re
from pathlib import Path


def run_tests():
    """Run pytest and generate XML report."""
    print("Running tests...")
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-v", "--junitxml=test_results/test_results.xml", "--tb=short"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0


def parse_test_results():
    """Parse JUnit XML and return test statuses."""
    xml_path = Path("test_results/test_results.xml")
    if not xml_path.exists():
        print("No test results XML found")
        return {}
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    test_statuses = {}
    
    # Handle both xunit1 and xunit2 formats
    for testcase in root.findall(".//testcase"):
        test_name = testcase.get("name", "")
        classname = testcase.get("classname", "")
        
        # Determine status
        status = "passed"
        if testcase.find("failure") is not None:
            status = "failed"
        elif testcase.find("error") is not None:
            status = "failed"
        elif testcase.find("skipped") is not None:
            status = "pending"
        
        # Extract test ID from test name (e.g., "test_1_1_..." -> "1.1")
        test_id = extract_test_id(test_name)
        if test_id:
            test_statuses[test_id] = status
    
    return test_statuses


def extract_test_id(test_name):
    """Extract test ID from test name like 'test_1_1_...' -> '1.1'."""
    # Match patterns like test_1_1, test_2_3, test_5_1, etc.
    match = re.search(r'test_(\d+)_(\d+)', test_name)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return None


def update_dashboard(test_statuses):
    """Update the dashboard HTML with test results."""
    dashboard_path = Path("test_results/test_dashboard.html")
    if not dashboard_path.exists():
        print("Dashboard not found")
        return
    
    content = dashboard_path.read_text()
    
    # Update each test status in the JavaScript test data array
    # The format is: { id: "1.1", ..., status: "pending", ... }
    for test_id, status in test_statuses.items():
        # Match the test object with this ID and update its status
        # Pattern matches: id: "X.Y", ... status: "old_status", ...
        # We need to match across multiple lines (DOTALL flag)
        # Match pattern: id: "1.1", ... status: "pending", ...
        pattern = rf'(id:\s*"{re.escape(test_id)}"[^}}]*?status:\s*")[^"]*(")'
        replacement = rf'\1{status}\2'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Update the loadTestStatuses function with default statuses
    if test_statuses:
        # Create default statuses object
        statuses_obj = "{\n"
        for test_id, status in sorted(test_statuses.items()):
            statuses_obj += f'                "{test_id}": "{status}",\n'
        statuses_obj = statuses_obj.rstrip(",\n") + "\n            }"
        
        # Replace the entire loadTestStatuses function
        new_function = f'''        function loadTestStatuses() {{
            // Default statuses from last test run (updated by run_tests_and_update_dashboard.py)
            const defaults = {statuses_obj};
            
            // First, apply defaults to all tests
            tests.forEach(test => {{
                if (defaults[test.id]) {{
                    test.status = defaults[test.id];
                }}
            }});
            
            // Then, override with saved localStorage values if they exist
            const saved = localStorage.getItem('testStatuses');
            if (saved) {{
                const statuses = JSON.parse(saved);
                tests.forEach(test => {{
                    if (statuses[test.id]) {{
                        test.status = statuses[test.id];
                    }}
                }});
            }}
        }}'''
        
        # Find and replace the function
        pattern = r'function loadTestStatuses\(\) \{[\s\S]*?\n        \}'
        content = re.sub(pattern, new_function, content)
    
    dashboard_path.write_text(content)
    print(f"Dashboard updated with {len(test_statuses)} test results")


def main():
    """Main function."""
    print("=" * 60)
    print("Running Tests and Updating Dashboard")
    print("=" * 60)
    
    # Run tests
    success = run_tests()
    
    # Parse results
    test_statuses = parse_test_results()
    print(f"\nParsed {len(test_statuses)} test results")
    
    # Update dashboard
    if test_statuses:
        update_dashboard(test_statuses)
        print("\n✅ Dashboard updated successfully!")
    else:
        print("\n⚠️  No test results to update")
    
    # Print summary
    passed = sum(1 for s in test_statuses.values() if s == "passed")
    failed = sum(1 for s in test_statuses.values() if s == "failed")
    pending = sum(1 for s in test_statuses.values() if s == "pending")
    
    print(f"\nSummary: {passed} passed, {failed} failed, {pending} pending")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())

