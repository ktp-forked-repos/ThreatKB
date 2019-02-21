'use strict';

angular.module('ThreatKB')
    .factory('Files', ['$resource', function ($resource) {
        return {
            resource: $resource('ThreatKB/files/:id', {}, {
                'query': {method: 'GET', isArray: true},
                'get': {method: 'GET'},
                'update': {method: 'PUT'},
		'delete': {method: 'DELETE'}
            }),
            ENTITY_MAPPING: {SIGNATURE: 1}
        };
    }]);
