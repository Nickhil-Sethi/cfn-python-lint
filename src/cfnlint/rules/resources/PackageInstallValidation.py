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
        config_resource_names = ['AWS::AutoScaling::LaunchConfiguration', 'AWS::EC2::Instance']

        str_resources = 'Resources'
        str_packages = 'packages'
        str_config = 'config'
        str_init = 'AWS::CloudFormation::Init'
        str_metadata = 'Metadata'
        matches = []

        resources = cfn.template.get(
            str_resources, {})

        for resource_name, resource in resources.items():
            if resource.get('Type') not in config_resource_names:
                continue
            
            metadata = resource.get(str_metadata)

            if not metadata:
                continue

            initobj = metadata.get(
                str_init)

            if not initobj:
                continue

            package_install = initobj.get(
                str_config, {}).get(
                str_packages)
            
            if not package_install:
                continue

            if not package_install.get('yum'):
                path_arr = [
                    str_resources,
                    resource_name,
                    str_metadata,
                    str_init,
                    str_config,
                    str_packages]

                path = ('/').join(
                    path_arr)
                
                message = \
                    f'{path} should have at least one of the following: (yum, apt)'

                matches.append(RuleMatch(
                    path_arr,
                    message))
        return matches
 
