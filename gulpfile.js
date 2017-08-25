var ftp = require('vinyl-ftp');
var gulp  = require('gulp');
var gutil = require('gulp-util');
var minimist = require('minimist');
var args = minimist(process.argv.slice(2));

gulp.task('deploy', function() {
  var remotePath = '/public_html/Visionari/';
  var conn = ftp.create({
    host: 'ftp.baywaylabs.it',
    user: args.user,
    password: args.password,
    log: gutil.log
  });
  gulp.src(['./html/**', '!./.*', '!./*.txt', '!./*.md', '!./*.js', '!./node_modules{,/**}', '!./doc{,/**}', '!./.git{,/**}'], { dot: true })
    .pipe(conn.newer(remotePath))
    .pipe(conn.dest(remotePath));
});