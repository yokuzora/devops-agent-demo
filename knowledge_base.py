KNOWN_ERRORS = {

    "No matching distribution found": {
        "root_cause": "Invalid package version",
        "suggestions": [
            "Check requirements.txt",
            "Verify package version exists",
            "Update dependency version"
        ]
    },

    "ModuleNotFoundError": {
        "root_cause": "Missing Python dependency",
        "suggestions": [
            "Install missing package",
            "Update requirements.txt",
            "Check virtual environment"
        ]
    },

    "ImagePullBackOff": {
        "root_cause": "Container image unavailable",
        "suggestions": [
            "Verify image tag",
            "Verify registry access",
            "Check image exists"
        ]
    },

    "permission denied": {
        "root_cause": "Permission issue",
        "suggestions": [
            "Check IAM permissions",
            "Check access tokens",
            "Verify service account"
        ]
    },

    "exit code 137": {
        "root_cause": "Out of memory",
        "suggestions": [
            "Increase memory",
            "Reduce workload",
            "Optimize build"
        ]
    }
}