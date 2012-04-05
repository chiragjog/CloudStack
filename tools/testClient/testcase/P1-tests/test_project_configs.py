# -*- encoding: utf-8 -*-
#
# Copyright (c) 2012 Citrix.  All rights reserved.
#
""" P1 tests for Project
"""
#Import Local Modules
from cloudstackTestCase import *
from cloudstackAPI import *
from testcase.libs.utils import *
from testcase.libs.base import *
from testcase.libs.common import *
import remoteSSHClient
import datetime


class Services:
    """Test Project Services
    """

    def __init__(self):
        self.services = {
                        "domain": {
                                   "name": "Domain",
                        },
                        "project": {
                                    "name": "Project",
                                    "displaytext": "Test project",
                        },
                         "mgmt_server": {
                                   "ipaddress": '192.168.100.21',
                                   "username": 'root',
                                   "password": 'fr3sca',
                                   "port": 22,     
                        },
                        "account": {
                                    "email": "administrator@clogeny.com",
                                    "firstname": "Test",
                                    "lastname": "User",
                                    "username": "test",
                                    # Random characters are appended for unique
                                    # username
                                    "password": "fr3sca",
                         },
                         "user": {
                                    "email": "mayur.dhande@clogeny.com",
                                    "firstname": "User",
                                    "lastname": "User",
                                    "username": "User",
                                    # Random characters are appended for unique
                                    # username
                                    "password": "fr3sca",
                         },
                         "service_offering": {
                                    "name": "Tiny Instance",
                                    "displaytext": "Tiny Instance",
                                    "cpunumber": 1,
                                    "cpuspeed": 100, # in MHz
                                    "memory": 64, # In MBs
                        },
                         "virtual_machine": {
                                    "displayname": "Test VM",
                                    "username": "root",
                                    "password": "password",
                                    "ssh_port": 22,
                                    "hypervisor": 'XenServer',
                                    # Hypervisor type should be same as
                                    # hypervisor type of cluster
                                    "privateport": 22,
                                    "publicport": 22,
                                    "protocol": 'TCP',
                         },
                         "template": {
                                "displaytext": "Public Template",
                                "name": "Public template",
                                "ostypeid": 'f9b709f2-e0fc-4c0f-80f1-b0494168f58d',
                                "url": "http://download.cloud.com/releases/2.0.0/UbuntuServer-10-04-64bit.vhd.bz2",
                                "hypervisor": 'XenServer',
                                "format" : 'VHD',
                                "isfeatured": True,
                                "ispublic": True,
                                "isextractable": True,
                        },
                        "configs": {
                                "project.invite.timeout": 300,
                        },
                        "mail_account": {
                                "server": 'imap.gmail.com',
                                "email": 'administrator@clogeny.com',
                                "password": 'fr3sca21!',
                                "folder": 'inbox',
                        },
                        "ostypeid": 'f9b709f2-e0fc-4c0f-80f1-b0494168f58d',
                        # Cent OS 5.3 (64 bit)
                        "sleep": 60,
                        "timeout": 10,
                        "mode":'advanced'
                    }


class TestUserProjectCreation(cloudstackTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_client = super(
                               TestUserProjectCreation,
                               cls
                               ).getClsTestClient().getApiClient()
        cls.services = Services().services
        # Get Zone
        cls.zone = get_zone(cls.api_client, cls.services)
        
        # Create domains, account etc.
        cls.domain = Domain.create(
                                   cls.api_client,
                                   cls.services["domain"]
                                   )

        cls.account = Account.create(
                            cls.api_client,
                            cls.services["account"],
                            admin=True,
                            domainid=cls.domain.id
                            )
        
        cls.user = Account.create(
                            cls.api_client,
                            cls.services["account"],
                            admin=True,
                            domainid=cls.domain.id
                            )
        
        cls._cleanup = [cls.account, cls.user, cls.domain]
        return

    @classmethod
    def tearDownClass(cls):
        try:
            #Cleanup resources used
            cleanup_resources(cls.api_client, cls._cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return

    def setUp(self):
        self.apiclient = self.testClient.getApiClient()
        self.dbclient = self.testClient.getDbConnection()
        self.cleanup = []
        return

    def tearDown(self):
        try:
            #Clean up, terminate the created accounts, domains etc
            cleanup_resources(self.apiclient, self.cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return


    def test_01_admin_project_creation(self):
        """Test create project as a domain admin and domain user
        """

        # Validate the following
        # 1. Check if 'allow.user.create.projects' configuration is true
        # 2. Create a Project as domain admin
        # 3. Create a Project as domain user
        # 4. In both 2 and 3 project creation should be successful 

        configs = Configurations.list(
                                      self.apiclient,
                                      name='allow.user.create.projects'
                                      )
        self.assertEqual(
                            isinstance(configs, list),
                            True,
                            "Check for a valid list configurations response"
                            )
        config = configs[0]
        self.assertEqual(
                            (config.value).lower(),
                            'true',
                            "'allow.user.create.projects' should be true"
                            )

        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        self.debug("Created project with domain admin with ID: %s" %
                                                                project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )

        self.assertEqual(
                            project.name,
                            list_project.name,
                            "Check project name from list response"
                            )
        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.user.account.name,
                                 domainid=self.user.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        self.debug("Created project with domain user with ID: %s" %
                                                            project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                        len(list_projects_reponse),
                        0,
                        "Check list project response returns a valid project"
                        )
        return
    @unittest.skip("Known bug-able to create project as a domain user")
    def test_02_user_project_creation(self):
        """Test create project as a domain admin and domain user
        """

        # Validate the following
        # 1. Check if 'allow.user.create.projects' configuration is false
        # 2. Create a Project as domain admin. Project creation should be
        #    successful.
        # 3. Create a Project as domain user. Project creation should fail

        configs = Configurations.list(
                                      self.apiclient,
                                      name='allow.user.create.projects'
                                      )
        self.assertEqual(
                            isinstance(configs, list),
                            True,
                            "Check for a valid list configurations response"
                            )
        config = configs[0]
        self.assertEqual(
                            (config.value).lower(),
                            'false',
                            "'allow.user.create.projects' should be true"
                            )

        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        self.debug("Created project with domain admin with ID: %s" %
                                                                project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )

        self.assertEqual(
                            project.name,
                            list_project.name,
                            "Check project name from list response"
                            )
        with self.assertRaises(Exception):
            project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.user.account.name,
                                 domainid=self.user.account.domainid
                                 )
            self.debug("Project creation with domain user: %s failed" %
                                                    self.user.account.name)
        return


class TestProjectInviteRequired(cloudstackTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_client = super(TestProjectInviteRequired, cls).getClsTestClient().getApiClient()
        cls.services = Services().services
        # Get Zone
        cls.zone = get_zone(cls.api_client, cls.services)
        
        # Create domains, account etc.
        cls.domain = get_domain(cls.api_client, cls.services)
        
        cls.account = Account.create(
                            cls.api_client,
                            cls.services["account"],
                            admin=True,
                            domainid=cls.domain.id
                            )
        
        cls.user = Account.create(
                            cls.api_client,
                            cls.services["user"],
                            admin=True,
                            domainid=cls.domain.id
                            )
        
        cls._cleanup = [cls.account, cls.user]
        return

    @classmethod
    def tearDownClass(cls):
        try:
            #Cleanup resources used
            cleanup_resources(cls.api_client, cls._cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return

    def setUp(self):
        self.apiclient = self.testClient.getApiClient()
        self.dbclient = self.testClient.getDbConnection()
        self.cleanup = []
        return

    def tearDown(self):
        try:
            #Clean up, terminate the created accounts, domains etc
            cleanup_resources(self.apiclient, self.cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return


    def test_03_add_user_to_project(self):
        """Add user to project when 'project.invite.required' is false"""
        
        # Validate the following:
        # 1. Create a Project
        # 2. Add users to the project. Verify user is added to project
        #    as regular user 

        # Verify 'project.invite.required' is set to false
        configs = Configurations.list(
                                      self.apiclient,
                                      name='project.invite.required'
                                      )
        self.assertEqual(
                            isinstance(configs, list),
                            True,
                            "Check for a valid list configurations response"
                            )
        config = configs[0]
        self.assertEqual(
                            (config.value).lower(),
                            'false',
                            "'project.invite.required' should be true"
                            )

        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        self.debug("Created project with domain admin with ID: %s" %
                                                                project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                        len(list_projects_reponse),
                        0,
                        "Check list project response returns a valid project"
                        )

        self.assertEqual(
                            project.name,
                            list_project.name,
                            "Check project name from list response"
                            )
        self.debug("Adding %s user to project: %s" % (
                                                      self.user.account.name,
                                                      project.name
                                                      ))
         # Add user to the project
        project.addAccount(
                           self.apiclient, 
                           self.user.account.name, 
                           self.user.account.email
                           )
        
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = Project.listAccounts(
                                            self.apiclient, 
                                            projectid=project.id,
                                            account=self.user.account.name,
                                            )
        self.debug(accounts_reponse)
        self.assertEqual(
                            isinstance(accounts_reponse, list),
                            True,
                            "Check for a valid list accounts response"
                            )
        
        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )
        account = accounts_reponse[0]
        
        self.assertEqual(
                            account.role,
                            'Regular',
                            "Newly added user is not added as a regular user"
                            )
        
        return

    def test_04_add_user_to_project(self):
        """Add user to project when 'project.invite.required' is true"""
        
        # Validate the following:
        # 1. Create a Project
        # 2. Add users to the project. verify user is shown in pending state

        # Verify 'project.invite.required' is set to false
        configs = Configurations.list(
                                      self.apiclient,
                                      name='project.invite.required'
                                      )
        self.assertEqual(
                            isinstance(configs, list),
                            True,
                            "Check for a valid list configurations response"
                            )
        config = configs[0]
        self.assertEqual(
                            (config.value).lower(),
                            'true',
                            "'project.invite.required' should be true"
                            )

        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        
        self.debug("Created project with domain admin with ID: %s" % 
                                                                project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                        len(list_projects_reponse),
                        0,
                        "Check list project response returns a valid project"
                        )

        self.assertEqual(
                            project.name,
                            list_project.name,
                            "Check project name from list response"
                            )
        self.debug("Adding %s user to project: %s" % (
                                                      self.user.account.name,
                                                      project.name
                                                      ))
         # Add user to the project
        project.addAccount(
                           self.apiclient, 
                           self.user.account.name, 
                           self.user.account.email
                           )
        
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = ProjectInvitation.list(
                                        self.apiclient,
                                        state='Pending',
                                        account=self.user.account.name,
                                        domainid=self.user.account.domainid
                                        )
        self.assertEqual(
                            isinstance(accounts_reponse, list),
                            True,
                            "Check for a valid list accounts response"
                            )
        
        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )
        account = accounts_reponse[0]
        
        self.assertEqual(
                    account.state,
                    'Pending',
                    "Newly added user is not added as a regular user"
                    )
        return

    def test_05_invitation_timeout(self):
        """Test global config project invitation timeout"""
        
        # Validate the following:
        # 1. Set configuration to 5 mins
        # 2. Create a Project 
        # 3. Add users to the project
        # 4. As a user accept invitation within 5 mins. Verify invitation is
        #    accepted and user become regular user of project
        
        # Verify 'project.invite.required' is set to false
        configs = Configurations.list(
                                      self.apiclient,
                                      name='project.invite.timeout'
                                      )
        self.assertEqual(
                            isinstance(configs, list),
                            True,
                            "Check for a valid list configurations response"
                            )
        config = configs[0]
        self.assertEqual(
                    int(config.value),
                    self.services["configs"]["project.invite.timeout"],
                    "'project.invite.timeout' should be %s" %
                            self.services["configs"]["project.invite.timeout"] 
                    )

        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        
        self.debug("Created project with domain admin with ID: %s" % 
                                                                project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                        len(list_projects_reponse),
                        0,
                        "Check list project response returns a valid project"
                        )

        self.assertEqual(
                            project.name,
                            list_project.name,
                            "Check project name from list response"
                            )
        self.debug("Adding %s user to project: %s" % (
                                                      self.user.account.name,
                                                      project.name
                                                      ))
         # Add user to the project
        project.addAccount(
                           self.apiclient, 
                           self.user.account.name, 
                           self.user.account.email
                           )
        
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = ProjectInvitation.list(
                                        self.apiclient,
                                        state='Pending',
                                        account=self.user.account.name,
                                        domainid=self.user.account.domainid
                                        )
        self.assertEqual(
                            isinstance(accounts_reponse, list),
                            True,
                            "Check for a valid list accounts response"
                            )
        
        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )
        account = accounts_reponse[0]
        
        self.assertEqual(
                    account.state,
                    'Pending',
                    "Newly added user is not added as a regular user"
                    )
        
        # Accept the invite
        ProjectInvitation.update(
                                 self.apiclient,
                                 projectid=project.id, 
                                 accept=True,
                                 account=self.user.account.name
                                 )
        self.debug(
            "Accepting project invitation for project: %s user: %s" % (
                                                      project.name,
                                                      self.user.account.name
                                                      ))
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = Project.listAccounts(
                                            self.apiclient, 
                                            projectid=project.id,
                                            account=self.user.account.name,
                                            )

        self.assertEqual(
                            isinstance(accounts_reponse, list),
                            True,
                            "Check for a valid list accounts response"
                            )
        
        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )
        account = accounts_reponse[0]
        
        self.assertEqual(
                            account.role,
                            'Regular',
                            "Newly added user is not added as a regular user"
                            )
        return

    def test_06_invitation_timeout_after_expiry(self):
        """Test global config project invitation timeout"""
        
        # Validate the following:
        # 1. Set configuration to 5 mins
        # 2. Create a Project 
        # 3. Add users to the project
        # 4. As a user accept invitation after 5 mins. Verify invitation is
        #    not accepted and is shown as expired
        
        # Verify 'project.invite.required' is set to false
        configs = Configurations.list(
                                      self.apiclient,
                                      name='project.invite.timeout'
                                      )
        self.assertEqual(
                            isinstance(configs, list),
                            True,
                            "Check for a valid list configurations response"
                            )
        config = configs[0]
        self.assertEqual(
                    int(config.value),
                    self.services["configs"]["project.invite.timeout"],
                    "'project.invite.timeout' should be %s" %
                            self.services["configs"]["project.invite.timeout"] 
                    )

        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        
        self.debug("Created project with domain admin with ID: %s" % 
                                                                project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                        len(list_projects_reponse),
                        0,
                        "Check list project response returns a valid project"
                        )

        self.assertEqual(
                            project.name,
                            list_project.name,
                            "Check project name from list response"
                            )
        self.debug("Adding %s user to project: %s" % (
                                                      self.user.account.name,
                                                      project.name
                                                      ))
         # Add user to the project
        project.addAccount(
                           self.apiclient, 
                           self.user.account.name, 
                           self.user.account.email
                           )
        
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = ProjectInvitation.list(
                                        self.apiclient,
                                        state='Pending',
                                        account=self.user.account.name,
                                        domainid=self.user.account.domainid
                                        )
        self.assertEqual(
                            isinstance(accounts_reponse, list),
                            True,
                            "Check for a valid list accounts response"
                            )
        
        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )
        account = accounts_reponse[0]
        
        self.assertEqual(
                    account.state,
                    'Pending',
                    "Newly added user is not added as a regular user"
                    )
        
        # sleep for 'project.invite.timeout' * 2 interval to wait for invite
        # to expire
        time.sleep(int(config.value) * 2)

        with self.assertRaises(Exception):
            # Accept the invite
            ProjectInvitation.update(
                                 self.apiclient,
                                 projectid=project.id, 
                                 accept=True,
                                 account=self.user.account.name
                                 )
            self.debug(
                "Accepting invitation after expiry project: %s user: %s" % (
                                                      project.name,
                                                      self.user.account.name
                                                      ))
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = ProjectInvitation.list(
                                        self.apiclient,
                                        account=self.user.account.name,
                                        domainid=self.user.account.domainid
                                        )

        self.assertEqual(
                            isinstance(accounts_reponse, list),
                            True,
                            "Check for a valid list accounts response"
                            )
        
        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )
        account = accounts_reponse[0]
        
        self.assertEqual(
                    account.state,
                    'Expired',
                    "Newly added user is not added as a regular user"
                    )
        return

    def test_07_invite_after_expiry(self):
        """Test global config project invitation timeout"""
        
        # Validate the following:
        # 1. Set configuration to 5 mins
        # 2. Create a Project 
        # 3. Add users to the project
        # 4. As a user accept invitation after 5 mins.
        # 5. Resend the invitation
        # 6. Verify invitation is sent again

        # Verify 'project.invite.required' is set to false
        configs = Configurations.list(
                                      self.apiclient,
                                      name='project.invite.timeout'
                                      )
        self.assertEqual(
                            isinstance(configs, list),
                            True,
                            "Check for a valid list configurations response"
                            )
        config = configs[0]
        self.assertEqual(
                    int(config.value),
                    self.services["configs"]["project.invite.timeout"],
                    "'project.invite.timeout' should be %s" %
                            self.services["configs"]["project.invite.timeout"] 
                    )

        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        
        self.debug("Created project with domain admin with ID: %s" % 
                                                                project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                        len(list_projects_reponse),
                        0,
                        "Check list project response returns a valid project"
                        )

        self.assertEqual(
                            project.name,
                            list_project.name,
                            "Check project name from list response"
                            )
        self.debug("Adding %s user to project: %s" % (
                                                      self.user.account.name,
                                                      project.name
                                                      ))
        # Add user to the project
        project.addAccount(
                           self.apiclient, 
                           self.user.account.name, 
                           self.user.account.email
                           )
        
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = ProjectInvitation.list(
                                        self.apiclient,
                                        state='Pending',
                                        account=self.user.account.name,
                                        domainid=self.user.account.domainid
                                        )
        self.assertEqual(
                            isinstance(accounts_reponse, list),
                            True,
                            "Check for a valid list accounts response"
                            )
        
        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )
        account = accounts_reponse[0]
        
        self.assertEqual(
                    account.state,
                    'Pending',
                    "Newly added user is not added as a regular user"
                    )
        
        # sleep for 'project.invite.timeout' * 2 interval to wait for invite
        # to expire
        time.sleep(int(config.value) * 2)

        self.debug("Adding %s user again to project: %s" % (
                                                      self.user.account.name,
                                                      project.name
                                                      ))
        # Add user to the project
        project.addAccount(
                           self.apiclient, 
                           self.user.account.name, 
                           self.user.account.email
                           )
        
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = ProjectInvitation.list(
                                        self.apiclient,
                                        state='Pending',
                                        account=self.user.account.name,
                                        domainid=self.user.account.domainid
                                        )
        self.assertEqual(
                            isinstance(accounts_reponse, list),
                            True,
                            "Check for a valid list accounts response"
                            )
        
        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )
        account = accounts_reponse[0]
        
        self.assertEqual(
                    account.state,
                    'Pending',
                    "Newly added user is not added as a regular user"
                    )
        return

    def test_08_decline_invitation(self):
        """Test decline invitation"""
        
        # Validate the following:
        # 1. Set configuration to 5 mins
        # 2. Create a Project 
        # 3. Add users to the project
        # 4. As a user decline invitation within 5 mins.
        # 5. Verify invitation is rejected and user doesn't become regular
        #    user.

        # Verify 'project.invite.required' is set to false
        configs = Configurations.list(
                                      self.apiclient,
                                      name='project.invite.timeout'
                                      )
        self.assertEqual(
                            isinstance(configs, list),
                            True,
                            "Check for a valid list configurations response"
                            )
        config = configs[0]
        self.assertEqual(
                    int(config.value),
                    self.services["configs"]["project.invite.timeout"],
                    "'project.invite.timeout' should be %s" %
                            self.services["configs"]["project.invite.timeout"] 
                    )

        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        
        self.debug("Created project with domain admin with ID: %s" % 
                                                                project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                        len(list_projects_reponse),
                        0,
                        "Check list project response returns a valid project"
                        )

        self.assertEqual(
                            project.name,
                            list_project.name,
                            "Check project name from list response"
                            )
        self.debug("Adding %s user to project: %s" % (
                                                      self.user.account.name,
                                                      project.name
                                                      ))
        # Add user to the project
        project.addAccount(
                           self.apiclient, 
                           self.user.account.name, 
                           self.user.account.email
                           )
        
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = ProjectInvitation.list(
                                        self.apiclient,
                                        state='Pending',
                                        account=self.user.account.name,
                                        domainid=self.user.account.domainid
                                        )
        self.assertEqual(
                            isinstance(accounts_reponse, list),
                            True,
                            "Check for a valid list accounts response"
                            )
        
        self.assertNotEqual(
                    len(list_projects_reponse),
                    0,
                    "Check list project response returns a valid project"
                    )
        account = accounts_reponse[0]
        
        self.assertEqual(
                    account.state,
                    'Pending',
                    "Newly added user is not added as a regular user"
                    )
        # Accept the invite
        ProjectInvitation.update(
                                 self.apiclient,
                                 projectid=project.id, 
                                 accept=False,
                                 account=self.user.account.name
                                 )
        self.debug(
                "Declining invitation for project: %s user: %s" % (
                                                      project.name,
                                                      self.user.account.name
                                                      ))
        # listProjectAccount to verify the user is added to project or not
        accounts_reponse = Project.listAccounts(
                                            self.apiclient, 
                                            projectid=project.id,
                                            account=self.user.account.name,
                                            )
        self.assertEqual(
                            accounts_reponse,
                            None,
                            "Check for a valid list accounts response"
                            )
        return
    @unittest.skip("Requires SMPT configs")
    def test_09_invite_to_project_by_email(self):
        """Test invite user to project by email"""
        
        # Validate the following:
        # 1. Set configuration to 5 mins
        # 2. Create a Project 
        # 3. Add users to the project
        # 4. As a user decline invitation within 5 mins.
        # 5. Verify invitation is rejected and user doesn't become regular
        #    user.

        # Verify 'project.invite.required' is set to false
        configs = Configurations.list(
                                      self.apiclient,
                                      name='project.invite.timeout'
                                      )
        self.assertEqual(
                            isinstance(configs, list),
                            True,
                            "Check for a valid list configurations response"
                            )
        config = configs[0]
        self.assertEqual(
                    int(config.value),
                    self.services["configs"]["project.invite.timeout"],
                    "'project.invite.timeout' should be %s" %
                            self.services["configs"]["project.invite.timeout"] 
                    )

        # Create project as a domain admin
        project = Project.create(
                                 self.apiclient,
                                 self.services["project"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )
        # Cleanup created project at end of test
        self.cleanup.append(project)
        
        self.debug("Created project with domain admin with ID: %s" % 
                                                                project.id)
        
        list_projects_reponse = Project.list(
                                             self.apiclient, 
                                             id=project.id,
                                             listall=True
                                             )

        self.assertEqual(
                            isinstance(list_projects_reponse, list),
                            True,
                            "Check for a valid list projects response"
                            )
        list_project = list_projects_reponse[0]

        self.assertNotEqual(
                        len(list_projects_reponse),
                        0,
                        "Check list project response returns a valid project"
                        )

        self.assertEqual(
                            project.name,
                            list_project.name,
                            "Check project name from list response"
                            )
        self.debug("Adding user with email: %s to project: %s" % (
                                                      self.user.account.email,
                                                      project.name
                                                      ))

        # Add user to the project
        project.addAccount(
                           self.apiclient,
                           email=self.user.account.user[0].email
                           )

        # Fetch the latest mail sent to user
        mail_content = fetch_latest_mail(
                                         self.services["mail_account"],
                                         from_mail=self.user.account.user[0].email
                                         )
        return
