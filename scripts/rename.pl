#!/usr/bin/perl

for ($i = 0; $i < 16; ++$i) {
    for ($j = 0; $j < 100; ++$j) {
        $old = sprintf("features/features_p%02d_r%02d.npy", $i, $j);
        $new = sprintf("features/features_p%02d_r%03d.npy", $i, $j);
        system "mv $old $new";
    }
}

for ($i = 0; $i < 16; ++$i) {
    for ($j = 0; $j < 100; ++$j) {
        $old = sprintf("indexes/indexes_p%02d_r%02d.txt", $i, $j);
        $new = sprintf("indexes/indexes_p%02d_r%03d.txt", $i, $j);
        system "mv $old $new";
    }
}

for ($j = 0; $j < 100; ++$j) {
    $old = sprintf("logs/main_r%02d.log", $j);
    $new = sprintf("logs/main_r%03d.log", $j);
    system "mv $old $new";
}
for ($j = 0; $j < 100; ++$j) {
    $old = sprintf("logs/error_r%02d.log", $j);
    $new = sprintf("logs/error_r%03d.log", $j);
    system "mv $old $new";
}
for ($j = 0; $j < 100; ++$j) {
    $old = sprintf("logs/detailed_r%02d.log", $j);
    $new = sprintf("logs/detailed_r%03d.log", $j);
    system "mv $old $new";
}
