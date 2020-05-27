import unittest

# Test files
from testing.LoggerTest import bb_LoggerTest, wb_LoggerTest
from testing.SnifferTest import bb_SnifferTest, wb_SnifferTest
from testing.Websocket_Client_Test import bb_ClientTest, wb_ClientTest
from testing.DetectorTest import bb_DetectorTest, wb_DetectorTest 
from testing.ModelTest import bb_ModelTest, wb_ModelTest
from testing.IntegrationTests import IntegrationTesting


if __name__ == '__main__':
    unittest.main()
