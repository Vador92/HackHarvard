#use this to collect data from user messages to correspond to a specific action
import requests
import FaceDatabase.facedb

# Replace with your Weaviate API URL
def validateFace(input_face_vector):
    # Perform a similarity search
    search_data = {
        "vector": input_face_vector,
        "k": 10  # Number of results to retrieve, adjust as needed
    }

    response = requests.post(f"{https://face-detection-v8iqjrfg.weaviate.network}/objects/similaritySearch", json=search_data)

    if response.status_code == 200:
        results = response.json().get("searchResults", [])

        # Filter results based on confidence threshold
        confidence_threshold = 0.90
        filtered_results = [result for result in results if result["certainty"] >= confidence_threshold]

        if filtered_results:
            # Return the filtered results
            print("Results above the 90% confidence threshold:")
            print(filtered_results)
        else:
            print("No results found above the 90% confidence threshold.")
    else:
        print("Failed to perform similarity search. Status code:", response.status_code)


validateFace([[[ 0 , 0]]

 [[ 0 ,78]]

 [[78, 78]]

 [[78 , 0]]])
