#!/usr/bin/perl
use Net::FTP;

if (@ARGV < 4) {
    print "ftpllnl.pl [get|put] dir start_run# stop_run#\n";
    exit;
}
$ftp = Net::FTP->new("ftp.llnl.gov", Debug=>0) or die "Cannot connect: $@";

$ftp->login("anonymous", '-anonymous@') or die "Cannot login ", $ftp->message;

$ftp->mkdir("outgoing/$ARGV[1]") if $ARGV[0] eq 'put';

$ftp->cwd("outgoing/$ARGV[1]") or die "Cannot change directory ", $ftp->message;

$ftp->binary() or die "Cannot change to binary mode ", $ftp->message;

for ($run = $ARGV[2]; $run <= @ARGV[3]; ++$run) {
    for ($part = 0; $part < 16; ++$part) {
        $file = sprintf("features_p%02d_r%03d.npy.bz2", $part, $run);
        
        if ($ARGV[0] eq 'put') {
            print "Putting $file ...\n";
            $ftp->put($file) or die "Cannot put ", $ftp->message;
        }
        else {
            print "Getting $file ...\n";
            $ftp->get($file) or die "Cannot get ", $ftp->message;
        }
    }
}
$ftp->quit;
