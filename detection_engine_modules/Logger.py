"""
The Logger Module.
"""

class Logger:
    """
    The Logger class intends to control the flow log and alert log file handles.

    Allows the opening and writing of the relevant data to their specific files.
    """
    def __init__(self):
        """
        The constructor of the Logger object.

        Attributes:
            alert_no (int): The incremental counter for the alert number.
            flow_file (None or 'obj':FILE): The flow file object storage.
            alert_file (None or 'obj':FILE): The alert file object storage.
            flow_file_name (string): The file name for the flow file.
            alert_file_name (string): The file name for the alert file.
        """
        self.alert_no = 1
        self.flow_file = None
        self.alert_file = None

        self.flow_file_name = "flows.binetflow"
        self.alert_file_name = "alerts.log"

        self.open_flow_file()
        self.open_alert_file()

    def __del__(self):
        """
        The Logger object's destructor.

        Explicitally closes the file handle objects.
        """
        print("Deleting Logger object and closing the file handles.")

        if self.flow_file and self.alert_file:
            self.flow_file.close()
            self.alert_file.close()

    def open_flow_file(self):
        """
        Creates a file handle for the flow log file, with the ability to write to the file.

        Returns:
            0: If successful.
        """
        # Uses 'self.flow_file_name' for the file name
        # Opens writeable file as 'self.file_handle'
        self.flow_file = open(self.flow_file_name, 'w')

        print("[ Logger ] Network Flow file successfully opened!")

        return 0

    def write_flow_to_file(self, flow_string):
        """
        Writes the flow data to the file.

        Args:
            flow_string (string): The flow string data that is to be written to the file.

        Returns:
            0: If successful.
        """
        # Write to file
        self.flow_file.write(flow_string + "\n")

        return 0

    def open_alert_file(self):
        """
        Creates a file handle for the alert log file, with the ability to write to the file.

        Returns:
            0: If successful.
        """
        # Uses 'self.alert_file_name' for the file name
        # Opens writeable file as 'self.file_handle'
        self.alert_file = open(self.alert_file_name, 'w')

        print("[ Logger ] Alert file successfully opened!")

        return 0

    def write_alert_to_file(self, alert):
        """
        Formats and writes the json alert data to the file.

        Args:
            alert (json-formatted string): The json-formatted alert data is to be written to the file.

        Returns:
            0: If successful.
        """
        # Write to file
        formatted_alert = "----- Alert #" + str(self.alert_no) + " -----"

        for key in alert:
            # Format data into a suitable format for file output
            # key + { values }
            line = key + " = " + str(alert[key])

            # Append line to the formatted_alert string
            formatted_alert += "\n" + line

        # Newline at end of alert output to space out alerts
        formatted_alert += "\n\n"

        # Print the formatted_alert output to the command line interface
        print(formatted_alert)

        # Write to file
        self.alert_file.write(formatted_alert)

        # Iterate alert_no
        self.alert_no += 1

        return 0
