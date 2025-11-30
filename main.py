# main.py
from parser import parse_log_text
from json_builder import build_fibo_payload
from fibo_client import generate_fibo_image

SAMPLE_LOG = """Users are not able to login to SmartStation in DEV after deployment.
We see 500 errors from AG and intermittent timeouts for SS.
Severity: High"""

def run_example():
    # Step 1: Parse the incident log
    parsed = parse_log_text(SAMPLE_LOG)
    print("Parsed Incident:", parsed)

    # Step 2: Build the FIBO payload
    payload = build_fibo_payload(parsed)
    payload["size"] = "1024x1024"  # Optional: set image size
    # Ensure prompt exists for API
    if "prompt" not in payload:
        payload["prompt"] = (
            f"Generate a clean, professional dashboard-ready incident image for:\n"
            f"- Service: {parsed.get('service')}\n"
            f"- Environment: {parsed.get('environment')}\n"
            f"- Severity: {parsed.get('severity')}\n"
            f"- Issue: {parsed.get('issue')}\n"
        )

    # Step 3: Generate the image
    print("\nSending request to BRIA/FIBO...")
    image_path = generate_fibo_image(payload)

    if image_path:
        print("\n✅ Image generation complete! Saved at:", image_path)
    else:
        print("\n❌ Failed to generate image. Check logs above.")

if __name__ == "__main__":
    run_example()
