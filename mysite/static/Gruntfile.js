module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
    
        concat: {   
            dist: {
                src: ['js/packages/*.js',      // angular and jquery 
                      'js/myAppController.js', // my code
                      'node_modules/angular-route/angular-route.min.js', 
                      'node_modules/angular-cookies/angular-cookies.min.js'
                     ],
                dest: 'js/build/production.js',
            }
        },
        // uglify = minify
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                src: 'js/build/production.js',
                dest: 'js/build/production.min.js'
            }
        }
    });
    
    // Load the plugin that provides the "uglify" task.
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    
    // Default task(s).
    grunt.registerTask('default', ['concat', 'uglify']);

};
