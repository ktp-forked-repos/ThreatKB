angular.module('ThreatKB')
    .controller('AuthController', ['$scope', '$document', '$location', 'AuthService', 'Cfg_settings', '$uibModal', 'Yara_rule', 'C2ip', 'C2dns', 'hotkeys',
        function ($scope, $document, $location, AuthService, Cfg_settings, $uibModal, Yara_rule, C2ip, C2dns, hotkeys) {
            $scope.isLoggedIn = AuthService.isLoggedIn;
            $scope.isAdmin = AuthService.isAdmin;
            $scope.user = AuthService.user;
            $scope.nav_image = Cfg_settings.get({key: "NAV_IMAGE"});

            $scope.search_artifacts = [];

            $scope.getPermalink = function (id, type_) {
                return $location.absUrl().split("/").slice(0, 4).join("/") + "/" + type_ + "/" + id;
            };

            $scope.select_artifact = function (selected) {
                $location.url(selected.url);
            }

            hotkeys.bindTo($scope)
                .add({
                    combo: 'ctrl+j',
                    description: 'Search',
                    allowIn: ['INPUT', 'SELECT', 'TEXTAREA'],
                    callback: function () {
                        //$document.find("input#focusser-0")[0].focus();
                        $scope.$broadcast('search_focus');
                    }
                });

            $scope.refresh_search = function (search) {
                if (!search) {
                    return;
                }

                $scope.search_artifacts = [];

                var dns_results = C2dns.query({
                    searches: {domain_name: search},
                    exclude_totals: true,
                    include_metadata: false
                });
                dns_results.$promise.then(function (results) {
                    results.forEach(function (c2dns) {
                        $scope.search_artifacts.push({
                            name: c2dns.domain_name,
                            url: "/c2dns/" + c2dns.id,
                            type: "c2dns"
                        })
                    });
                }, function (error) {
                    console.log(error);
                });

                var yara_results = Yara_rule.resource.query({
                    searches: {name: search},
                    exclude_totals: true,
                    include_metadata: false
                });
                yara_results.$promise.then(function (results) {
                    results.forEach(function (yara_rule) {
                        $scope.search_artifacts.push({
                            name: yara_rule.name,
                            url: "/yara_rule/" + yara_rule.id,
                            type: "yara_rule"
                        })
                    });
                }, function (error) {
                    console.log(error);
                });

                var ip_results = C2ip.query({searches: {ip: search}, exclude_totals: true, include_metadata: false});
                ip_results.$promise.then(function (results) {
                    results.forEach(function (c2ip) {
                        $scope.search_artifacts.push({
                            name: c2ip.ip,
                            url: "/c2ips/" + c2ip.id,
                            type: "c2ip"
                        })
                    });

                }, function (error) {
                    console.log(error);
                });

            };

            $scope.login = function () {
                // initial values
                $scope.error = false;
                $scope.disabled = true;

                // call login from service
                AuthService.login($scope.login_form.email, $scope.login_form.password)
                    .then(function () {
                        $location.path('/');
                        $scope.disabled = false;
                        $scope.loginForm = {};
                    })
                    .catch(function () {
                        $scope.error = true;
                        $scope.errorMessage = "Invalid username and/or password";
                        $scope.disabled = false;
                        $scope.login_form = {};
                    });
            };

            $scope.logout = function () {
                // call logout from service
                AuthService.logout()
                    .then(function () {
                        $location.path('/login');
                    });

            };

        }])
    .controller('UsersController', ['$scope', '$uibModal', 'resolvedUsers', 'UserService',
        function ($scope, $uibModal, resolvedUsers, UserService) {
            $scope.users = resolvedUsers;
            $scope.user = {};
            $scope.user.passwordConfirm = "";


            $scope.create = function () {
                $scope.clear();
                $scope.open();
            };

            $scope.update = function (id) {
                $scope.user = UserService.get({id: id});
                $scope.users = UserService.query({include_inactive: 1});
                $scope.open(id);
            };

            $scope.save = function (id) {
                if (id) {
                    UserService.update({id: id}, $scope.user, function () {
                        $scope.users = UserService.query({include_inactive: 1});
                    });
                } else {
                    UserService.save($scope.user, function () {
                        $scope.users = UserService.query({include_inactive: 1});
                    });
                }
            };

            $scope.clear = function () {
                $scope.user = {
                    "email": "",
                    "password": "",
                    "passwordConfirm": "",
                    "admin": false,
                    "active": true,
                    "registered_on": ""
                };
            };

            $scope.open = function (id) {
                var userSave = $uibModal.open({
                    templateUrl: 'users-save.html',
                    controller: 'UsersSaveController',
                    resolve: {
                        user: function () {
                            return $scope.user;
                        }
                    }
                });

                userSave.result.then(function (user) {
                    $scope.user = user;
                    $scope.save(id);
                });
            };
        }])
    .controller('UsersSaveController', ['$scope', '$http', '$uibModalInstance', 'user',
        function ($scope, $http, $uibModalInstance, user) {
            $scope.user = user;
            $scope.user.passwordConfirm = "";

            $scope.ok = function () {
                $uibModalInstance.close($scope.user);
            };

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };

            $scope.setAdmin = function (val) {
                $scope.user.admin = val;
            };

            $scope.setActive = function (val) {
                $scope.user.active = val;
            };
        }]);
