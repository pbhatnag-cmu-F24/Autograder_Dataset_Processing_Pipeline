import sys
from pathlib import Path
from flask import Blueprint, request, jsonify

# Ensure project modules are in sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.services.file_filtering_service import file_ext_filter, file_name_filter

# Define the blueprint for filtering endpoints
filter_bp = Blueprint("filter_bp", __name__)

# Controller for file extension filtering
@filter_bp.route("/api/filter/fileext", methods=["POST"])
def filter_file_extension():
    """
    Clears the raw unzipped folder, then filters files in data/unzipped based on their extension.
    Filter parameters (filter_type and filter_list) are provided in the JSON request body.
    The filtered files are saved to data/file_filtered.
    """
    # Hardcoded paths
    SOURCE_FOLDER = Path("data/unzipped")
    DEST_FOLDER = Path("data/file_filtered")
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    filter_type = data.get("filter_type")
    filter_list = data.get("filter_list")

    if filter_type not in ["in", "out"]:
        return jsonify({"error": "Invalid filter type, must be 'in' or 'out'"}), 400
    if not isinstance(filter_list, list):
        return jsonify({"error": "filter_list must be a list"}), 400

    try:
        # Call file_ext_filter from the service; assumed to return a list of filtered file paths
        result = file_ext_filter(SOURCE_FOLDER, filter_list, filter_type, DEST_FOLDER)
        return jsonify({
            "message": "File extension filtering complete",
            "filtered_files": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controller for filename filtering
@filter_bp.route("/api/filter/filename", methods=["POST"])
def filter_filename():
    """
    Filters files in data/file_filtered based on the filename.
    The filtering parameters (filter_type and filter_list) are provided in the JSON request body.
    """
    # Hardcoded path for filename filtering
    SOURCE_FOLDER = Path("data/file_filtered")
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    filter_type = data.get("filter_type")
    filter_list = data.get("filter_list")

    if filter_type not in ["in", "out"]:
        return jsonify({"error": "Invalid filter type, must be 'in' or 'out'"}), 400
    if not isinstance(filter_list, list):
        return jsonify({"error": "filter_list must be a list"}), 400

    try:
        # Call file_name_filter from the service; assumed to return a list of filtered file paths
        result = file_name_filter(SOURCE_FOLDER, filter_list, filter_type)
        return jsonify({
            "message": "Filename filtering complete",
            "filtered_files": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
