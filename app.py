#!/usr/bin/env python3
import aws_cdk as cdk
from ip_tracker_stack.ip_tracker_stack import IpTrackerStack

app = cdk.App()
IpTrackerStack(app, "IpTrackerStack")
app.synth()
