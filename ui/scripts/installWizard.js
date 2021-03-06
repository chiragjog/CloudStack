(function($, cloudStack) {
  cloudStack.installWizard = {
    // Check if install wizard should be invoked
    check: function(args) {
      $.ajax({
        url: createURL('listZones'),
        dataType: 'json',
        async: true,
        success: function(data) {
          args.response.success({
            doInstall: !data.listzonesresponse.zone
          });
        }
      });
    },

    changeUser: function(args) {
      $.ajax({
        url: createURL('updateUser'),
        data: {
          id: cloudStack.context.users[0].userid,
          password: md5Hashed ? $.md5(args.data.password) : todb(args.data.password)
        },
        dataType: 'json',
        async: true,
        success: function(data) {
          args.response.success({
            data: { newUser: data.updateuserresponse.user }
          });
        }
      });
    },

    // Copy text
    copy: {
      // Tooltips
      'tooltip.addZone.name': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addZone.name'
        });
      },

      'tooltip.addZone.dns1': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addZone.dns1'
        });
      },

      'tooltip.addZone.dns2': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addZone.dns2'
        });
      },

      'tooltip.addZone.internaldns1': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addZone.internaldns1'
        });
      },

      'tooltip.addZone.internaldns2': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addZone.internaldns2'
        });
      },

      'tooltip.configureGuestTraffic.name': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.configureGuestTraffic.name'
        });
      },

      'tooltip.configureGuestTraffic.description': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.configureGuestTraffic.description'
        });
      },

      'tooltip.configureGuestTraffic.guestGateway': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.configureGuestTraffic.guestGateway'
        });
      },

      'tooltip.configureGuestTraffic.guestNetmask': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.configureGuestTraffic.guestNetmask'
        });
      },

      'tooltip.configureGuestTraffic.guestStartIp': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.configureGuestTraffic.guestStartIp'
        });
      },

      'tooltip.configureGuestTraffic.guestEndIp': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.configureGuestTraffic.guestEndIp'
        });
      },

      'tooltip.addPod.name': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addPod.name'
        });
      },

      'tooltip.addPod.reservedSystemGateway': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addPod.reservedSystemGateway'
        });
      },

      'tooltip.addPod.reservedSystemNetmask': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addPod.reservedSystemNetmask'
        });
      },

      'tooltip.addPod.reservedSystemStartIp': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addPod.reservedSystemStartIp'
        });
      },

      'tooltip.addPod.reservedSystemEndIp': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addPod.reservedSystemEndIp'
        });
      },

      'tooltip.addCluster.name': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addCluster.name'
        });
      },

      'tooltip.addHost.hostname': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addHost.hostname'
        });
      },

      'tooltip.addHost.username': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addHost.username'
        });
      },

      'tooltip.addHost.password': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addHost.password'
        });
      },

      'tooltip.addPrimaryStorage.name': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addPrimaryStorage.name'
        });
      },

      'tooltip.addPrimaryStorage.server': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addPrimaryStorage.server'
        });
      },

      'tooltip.addPrimaryStorage.path': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addPrimaryStorage.path'
        });
      },

      'tooltip.addSecondaryStorage.nfsServer': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addSecondaryStorage.nfsServer'
        });
      },

      'tooltip.addSecondaryStorage.path': function(args) {
        args.response.success({
          text: 'message.installWizard.tooltip.addSecondaryStorage.path'
        });
      },

      // Intro text
      whatIsCloudStack: function(args) {
        args.response.success({
          text: 'message.installWizard.copy.whatIsCloudStack'
        });
      },

      // EULA
      eula: function(args) {
        args.response.success({
          text: '<iframe src="eula.html" />'
        });
      },

      whatIsAZone: function(args) {
        args.response.success({
          text: 'message.installWizard.copy.whatIsAZone'
        });
      },

      whatIsAPod: function(args) {
        args.response.success({
          text: 'message.installWizard.copy.whatIsAPod'
        });
      },

      whatIsACluster: function(args) {
        args.response.success({
          text: 'message.installWizard.copy.whatIsACluster'
        });
      },

      whatIsAHost: function(args) {
        args.response.success({
          text: 'message.installWizard.copy.whatIsAHost'
        });
      },

      whatIsPrimaryStorage: function(args) {
        args.response.success({
          text: 'message.installWizard.copy.whatIsPrimaryStorage'
        });
      },

      whatIsSecondaryStorage: function(args) {
        args.response.success({
          text: 'message.installWizard.copy.whatIsSecondaryStorage'
        });
      }
    },

    action: function(args) {
      var success = args.response.success;
      var message = args.response.message;
      
      // Get default network offering
      var selectedNetworkOffering;
      $.ajax({
        url: createURL("listNetworkOfferings&state=Enabled&guestiptype=Shared"),
        dataType: "json",
        async: false,
        success: function(json) {
          selectedNetworkOffering = $.grep(
            json.listnetworkofferingsresponse.networkoffering,
            function(networkOffering) {
              var services = $.map(networkOffering.service, function(service) {
                return service.name;
              });
							
              //pick the network offering including SecurityGroup, but excluding Lb and StaticNat. (bug 13665)
              return (($.inArray('SecurityGroup', services) != -1) && ($.inArray('Lb', services) == -1) && ($.inArray('StaticNat', services) == -1)) ;
            }
          )[0];					
        }
      });
     
      cloudStack.zoneWizard.action($.extend(true, {}, args, {
        // Plug in hard-coded values specific to quick install
        data: {
          zone: {
            networkType: 'Basic',
            domain: 1,
            networkOfferingId: selectedNetworkOffering.id
          },
					pluginFrom: {
					  name: 'installWizard',
						selectedNetworkOfferingHavingSG: true
					}						
        },
        response: {
          success: function(args) {
            var enableZone = function() {
              message('Enabling zone...');
              cloudStack.zoneWizard.enableZoneAction({
                data: args.data,
                formData: args.data,
                launchData: args.data,
                response: {
                  success: function(args) {
                    pollSystemVMs();
                  }
                }
              });              
            };

            var pollSystemVMs = function() {
              // Poll System VMs, then enable zone
              message('Creating system VMs (this may take a while)');
              var poll = setInterval(function() {
                $.ajax({
                  url: createURL('listSystemVms'),
                  success: function(data) {
                    var systemVMs = data.listsystemvmsresponse.systemvm;

                    if (systemVMs && systemVMs.length > 1) {
                      if (systemVMs.length == $.grep(systemVMs, function(vm) {
                        return vm.state == 'Running';
                      }).length) {
                        clearInterval(poll);
                        message('System VMs ready.');
                        setTimeout(pollBuiltinTemplates, 500);
                      }
                    }
                  }
                });
              }, 5000);
            };

            // Wait for builtin template to be present -- otherwise VMs cannot launch
            var pollBuiltinTemplates = function() {
              message('Waiting for builtin templates to load...');
              var poll = setInterval(function() {
                $.ajax({
                  url: createURL('listTemplates'),
                  data: {
                    templatefilter: 'all'
                  },
                  success: function(data) {
                    var templates = data.listtemplatesresponse.template ?
                      data.listtemplatesresponse.template : [];
                    var builtinTemplates = $.grep(templates, function(template) {
                      return template.templatetype == 'BUILTIN';
                    });

                    if (builtinTemplates.length) {
                      clearInterval(poll);
                      message('Your CloudStack is ready!');
                      setTimeout(success, 1000);
                    }
                  }
                });
              }, 5000);
            };

            enableZone();
          }
        }
      }));
    }
  };
}(jQuery, cloudStack));
