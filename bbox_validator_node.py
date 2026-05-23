import torch

class SAM3BBoxValidator:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bboxes": ("BOUNDING_BOX",),
                "check_mode": (["any_detected", "min_score_detected", "min_area_detected", "count_at_least"], {
                    "default": "any_detected"
                }),
                "min_score": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "min_area": ("INT", {"default": 0, "min": 0, "max": 10000000, "step": 10}),
                "min_count": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "INT", "STRING")
    RETURN_NAMES = ("boolean", "int_value", "string_value")
    FUNCTION = "validate_bbox"
    CATEGORY = "utils/logic"

    def validate_bbox(self, bboxes, check_mode, min_score=0.5, min_area=0, min_count=1):
        # bboxes is list[list[dict]] from SAM3 Detect.
        # Handling edge cases where bboxes is None or empty list
        if bboxes is None:
            return (False, 0, "false")

        # Normalize the list of frames
        # If it's a single frame dict instead of a list of frames, wrap it.
        # SAM3 output is list[list[dict]] but just in case, let's make it robust:
        frames = []
        if isinstance(bboxes, dict):
            frames = [[bboxes]]
        elif isinstance(bboxes, list):
            for item in bboxes:
                if isinstance(item, list):
                    frames.append(item)
                elif isinstance(item, dict):
                    # It's a single list of dicts, let's treat it as a frame list of dicts
                    frames.append([item])
        else:
            # Fallback for unexpected formats
            return (False, 0, "false")

        result = False

        if check_mode == "any_detected":
            # True if any frame has at least one bounding box detected
            result = any(len(frame) > 0 for frame in frames)

        elif check_mode == "min_score_detected":
            # True if any bounding box in any frame has score >= min_score
            for frame in frames:
                for box in frame:
                    if isinstance(box, dict) and box.get("score", 0.0) >= min_score:
                        result = True
                        break
                if result:
                    break

        elif check_mode == "min_area_detected":
            # True if any bounding box in any frame has width * height >= min_area
            for frame in frames:
                for box in frame:
                    if isinstance(box, dict):
                        w = box.get("width", 0.0)
                        h = box.get("height", 0.0)
                        if (w * h) >= min_area:
                            result = True
                            break
                if result:
                    break

        elif check_mode == "count_at_least":
            # True if any frame has at least min_count bounding boxes
            result = any(len(frame) >= min_count for frame in frames)

        int_val = 1 if result else 0
        str_val = "true" if result else "false"

        return (result, int_val, str_val)

# Export the node mappings
NODE_CLASS_MAPPINGS = {
    "SAM3BBoxValidator": SAM3BBoxValidator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SAM3BBoxValidator": "SAM3 BBox Validator"
}
