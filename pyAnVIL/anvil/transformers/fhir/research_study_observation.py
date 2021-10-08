"""Represent fhir entity."""

from anvil.transformers.fhir import make_identifier

logged_already = []


class ResearchStudyObservation:
    """Create fhir entity."""

    class_name = "observation"
    resource_type = "Observation"

    @staticmethod
    def build_entity(workspace):
        """Create FHIR entity."""
        slug = make_identifier(workspace.id)

        entity = {
            "resourceType": "Observation",
            "id": slug,
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "https://www.ncbi.nlm.nih.gov/fhir",
                        "code": "Summary",
                        "display": "Variable Summary"
                    }
                ]
            },
            "focus": [
                {
                    "reference": f"ResearchStudy/{make_identifier(workspace.id)}"
                }
            ],
            "component": [
                # {
                # "code": {
                #     "coding": [
                #     {
                #         "code": "CohortCount",
                #         "display": "Number of Cohorts"
                #     }
                #     ]
                # },
                # "valueInteger": 41
                # },
                {
                    "code": {
                        "coding": [
                            {
                                "system": "https://www.ncbi.nlm.nih.gov/fhir",
                                "code": "SampleCount",
                                "display": "Number of Samples"
                            }
                        ]
                    },
                    "valueInteger": len(workspace.samples)
                },
                {
                    "code": {
                        "coding": [
                            {
                                "system": "https://www.ncbi.nlm.nih.gov/fhir",
                                "code": "Participant",
                                "display": "Number of Participants"
                            }
                        ]
                    },
                    "valueInteger": len(workspace.subjects)
                },
                {
                    "code": {
                        "coding": [
                            {
                                "code": "StorageSize",
                                "display": "Size on Disk"
                            }
                        ]
                    },
                    "valueQuantity": {
                        "value": sum(workspace.blob_sizes.values()),
                        "system": "http://unitsofmeasure.org",
                        "code": "L"
                    }
                }
            ]
        }
        return entity
