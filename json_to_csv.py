import pandas as pd
import json

def calculate_messages(data):
    """
    Calculate the number of messages sent and received for each user.

    Parameters
    ----------
    data : list of dict
        A list of dictionaries where each dictionary contains user data.

    Returns
    -------
    list of tuple
        A list of tuples, each containing the user ID, number of messages sent, and number of messages received.
    """
    rows = []
    for item in data:
        _id = item["_id"]
        messages = item["messages"]
        no_of_msgs_sent = sum(messages["sent"].values())
        no_of_msgs_received = sum(messages["received"].values())
        row = (_id, no_of_msgs_sent, no_of_msgs_received)
        rows.append(row)
    return rows

def calculate_matches(data):
    """
    Calculate the number of days and matches for each user.

    Parameters
    ----------
    data : list of dict
        A list of dictionaries where each dictionary contains user data.

    Returns
    -------
    list of tuple
        A list of tuples, each containing the user ID, number of days, and number of matches.
    """
    rows = []
    for item in data:
        _id = item["_id"]
        matches = item["matches"]
        no_of_days = len(matches)
        no_of_matches = sum(matches.values())
        row = (_id, no_of_days, no_of_matches)
        rows.append(row)
    return rows

def calculate_swipes(data):
    """
    Calculate the total swipe likes and passes for each user.

    Parameters
    ----------
    data : list of dict
        A list of dictionaries where each dictionary contains user data.

    Returns
    -------
    list of tuple
        A list of tuples, each containing the user ID, total swipe likes, and total swipe passes.
    """
    rows = []
    for item in data:
        _id = item["_id"]
        swipe_likes = item["swipeLikes"]
        swipe_passes = item["swipePasses"]
        total_swipe_likes = sum(swipe_likes.values())
        total_swipe_passes = sum(swipe_passes.values())
        row = (_id, total_swipe_likes, total_swipe_passes)
        rows.append(row)
    return rows

def extract_user_info(data):
    """
    Extract user information from the data.

    Parameters
    ----------
    data : list of dict
        A list of dictionaries where each dictionary contains user data.

    Returns
    -------
    list of tuple
        A list of tuples, each containing user information such as ID, birth date, age filters, location, and more.
    """
    rows = []
    for item in data:
        _id = item["_id"]
        user = item["user"]
        birth_date = user.get("birthDate", None)
        age_filter_min = user.get("ageFilterMin", None)
        age_filter_max = user.get("ageFilterMax", None)
        city_name = user.get("cityName", None)
        country = user.get("country", None)
        create_date = user.get("createDate", None)
        education = user.get("education", None)
        gender = user.get("gender", None)
        interested_in = user.get("interestedIn", None)
        gender_filter = user.get("genderFilter", None)
        instagram = user.get("instagram", None)
        spotify = user.get("spotify", None)
        jobs = user.get("jobs", [])
        job_title = jobs[0].get("title", None) if jobs else None
        education_level = user.get("educationLevel", None)
        
        row = (_id, birth_date, age_filter_min, age_filter_max, city_name, country, create_date, education, gender, interested_in, gender_filter, instagram, spotify, job_title, education_level)
        rows.append(row)
    return rows

def main():
    """
    Main function to read JSON data, process it, and save it as a CSV file.

    This function reads user data from a JSON file, calculates various statistics,
    and merges them into a single DataFrame which is then saved as a CSV file.
    """
    # Read the JSON file
    json_path = "profiles_2021-11-10.json"
    with open(json_path, 'r') as file:
        data = json.load(file)

        # Extract the required information
        rows = []
        for item in data:
            _id = item["_id"]
            app_opens = item["appOpens"]
            sum_app_opens = sum(app_opens.values())
            no_of_days = len(app_opens)
            conversations_meta = item["conversationsMeta"]
            row = (
                _id,
                sum_app_opens,
                no_of_days,
                conversations_meta["nrOfConversations"],
                conversations_meta["longestConversation"],
                conversations_meta["longestConversationInDays"],
                conversations_meta["averageConversationLength"],
                conversations_meta["averageConversationLengthInDays"],
                conversations_meta["medianConversationLength"],
                conversations_meta["medianConversationLengthInDays"],
                conversations_meta["nrOfOneMessageConversations"],
                conversations_meta["percentOfOneMessageConversations"],
                conversations_meta["nrOfGhostingsAfterInitialMessage"],
            )
            rows.append(row)

        # Define the columns
        columns = [
            "_id",
            "sum_app_opens",
            "no_of_days",
            "nrOfConversations",
            "longestConversation",
            "longestConversationInDays",
            "averageConversationLength",
            "averageConversationLengthInDays",
            "medianConversationLength",
            "medianConversationLengthInDays",
            "nrOfOneMessageConversations",
            "percentOfOneMessageConversations",
            "nrOfGhostingsAfterInitialMessage",
        ]

        # Create a DataFrame with the extracted information
        df = pd.DataFrame(rows, columns=columns)

        # Calculate no_of_days and no_of_matches
        matches_rows = calculate_matches(data)

        # Define the columns
        matches_columns = ["_id", "no_of_days", "no_of_matches"]

        # Create a DataFrame with the extracted information
        matches_df = pd.DataFrame(matches_rows, columns=matches_columns)

        # Merge with the existing DataFrame
        final_df = pd.merge(df, matches_df, on="_id", how="left")

        # Calculate no_of_msgs_sent and no_of_msgs_received
        messages_rows = calculate_messages(data)

        # Define the columns
        messages_columns = ["_id", "no_of_msgs_sent", "no_of_msgs_received"]

        # Create a DataFrame with the extracted information
        messages_df = pd.DataFrame(messages_rows, columns=messages_columns)

        # Merge with the existing DataFrame
        final_df = pd.merge(final_df, messages_df, on="_id", how="left")

        # Calculate swipe_likes and swipe_passes
        swipes_rows = calculate_swipes(data)

        # Define the columns
        swipes_columns = ["_id", "swipe_likes", "swipe_passes"]

        # Create a DataFrame with the extracted information
        swipes_df = pd.DataFrame(swipes_rows, columns=swipes_columns)

        # Merge with the existing DataFrame
        final_df = pd.merge(final_df, swipes_df, on="_id", how="left")

        # Extract user information
        user_rows = extract_user_info(data)

        # Define the columns
        user_columns = ["_id", "birthDate", "ageFilterMin", "ageFilterMax", "cityName", "country", "createDate", "education", "gender", "interestedIn", "genderFilter", "instagram", "spotify", "jobTitle", "educationLevel"]

        # Create a DataFrame with the extracted information
        user_df = pd.DataFrame(user_rows, columns=user_columns)

        # Merge with the existing DataFrame
        final_df = pd.merge(final_df, user_df, on="_id", how="left")

        df = final_df.copy()

        df.to_csv('Tinder_Data_v2.csv', index=False)

if __name__ == '__main__':
    main()
