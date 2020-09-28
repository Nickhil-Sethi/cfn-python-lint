"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""
from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch

class PackageInstallationValid(CloudFormationLintRule):
    """Check if Metadata Init has common errors"""

    id = 'E9999'
    experimental = True
    shortdesc = 'Metadata Init Config has appropriate properties'
    description = 'Metadata Init Config has appropriate properties'
    source_url = '' # 'https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-interface.html'
    tags = ['init']

    
    def match(self, cfn):
        """Check CloudFormation Metadata Interface Configuration"""
        config_resource_names = ['AWS::AutoScaling::LaunchConfiguration']
        print(self.logger)
        self.logger.debug("hello: we in here")
        matches = []

        strinit = 'AWS::CloudFormation::Init'
        resources = cfn.template.get(
            'Resources', {})

        for resource_name, resource in resources.items():
            if resource.get('Type') not in config_resource_names:
                continue
            metadata = resource.get('Metadata')
            if not metadata:
                continue
            initobj = metadata.get('AWS::CloudFormation::Init')
            if not initobj:
                continue
            package_install = initobj.get(
                'config', {}).get('packages')
            if not package_install:
                continue
            if not package_install.get('yum'):
                matches.append(RuleMatch(
                    ['Resources', resource_name,'Metadata','AWS::CloudFormation::Init','config','packages'], 'this sucks'))
                print(resource_name, resource)
        return matches
 
