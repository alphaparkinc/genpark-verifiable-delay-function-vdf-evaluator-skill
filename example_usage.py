"""Example usage for Verifiable Delay Function Skill."""
from client import VerifiableDelayFunction

def main():
    print("Executing Verifiable Delay Function...")
    seed = 889900
    steps = 500
    output, proof = VerifiableDelayFunction.evaluate(seed, steps)
    print(f"Computed VDF output after {steps} steps: {output}")
    print("Proof:", proof)

    valid = VerifiableDelayFunction.verify(seed, steps, output, proof)
    print("Verification:", valid)
    assert valid == True, "VDF verification failed"
    print("Verifiable Delay Function verified successfully!")

if __name__ == "__main__":
    main()
