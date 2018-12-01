var gulp = require('gulp'),
    sass = require('gulp-sass'),
    concat = require('gulp-concat'),
    clean = require('gulp-clean-css'),
    rename = require('gulp-rename'),
    uglify = require('gulp-uglify'),
    rm = require('gulp-rimraf');


//file paths
var scssFiles = './application/static/src/scss/**/*.scss',
    cssDest = './application/static/css/',
    jsFiles = [
        './application/static/src/js/jquery.min.js',
        './application/static/src/js/bootstrap.min.js',
        './application/static/src/js/jquery.themepunch.tools.min.js',
        './application/static/src/js/jquery.mixitup.min.js',
        './application/static/src/js/wow.js',
        './application/static/src/js/custom.js',
    ],
    jsDest = './application/static/js/';


gulp.task('sass', function(){
    return gulp.src(scssFiles)
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(cssDest));
});


gulp.task('minify-css', ['sass'], function() {
    gulp.src('./application/static/css/main.css')
        .pipe(clean({
            debug: true,
            inline: ['none'],
        })
        // .pipe(rename({
        //   suffix: '.min',
        // }))
        .pipe(gulp.dest(cssDest)));
});


gulp.task('scripts', function() {
    return gulp.src(jsFiles)
        .pipe(concat('main.js'))
        .pipe(gulp.dest(jsDest));
});


gulp.task('minify-js', ['scripts'], function () {
    gulp.src('./application/static/js/main.js')
        .pipe(uglify())
        .pipe(gulp.dest(jsDest));
});


gulp.task('clean', function() {
    return gulp.src([
            './application/static/css/main.css',
            './application/static/js/main.js',
        ])
        .pipe(rm());
});


gulp.task('watch', function() {
    gulp.watch(scssFiles, ['sass']),
    gulp.watch(jsFiles, ['scripts']);
});

gulp.task('default', ['sass', 'scripts', 'watch']);

gulp.task('build', ['clean', 'minify-css', 'minify-js']);