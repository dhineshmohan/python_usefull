#!/usr/bin/perl
use strict;
use Redis::Client;
use Redis;
use JSON;
use Config::Simple;
use TaskCreator qw(create_task write_log);

#my $conn = Redis::Client->new( host => 'localhost', port => 6379 );
my $b = '{"processingType" : "STATEMENT", "perfiosTransactionId" : "A123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "PRODUCTION"}';
#my $len = $conn->rpush(my_list => $b);
#print "$len\n";
my $r = Redis->new(server => 'localhost:6379');
#$r->auth('falcon123');
#$r->lpush('my_list', $b);
my $er = $r->lpop('test_qu');
print $er . "\n";


=h
my ($manager_id, $serial, $file);
my @bank_list = ('Shankar', 'Harishkumar', 'Varun', 'Peter', 'Premkumar', 'Sahana', 'Shilpa', 'Shivanna', 'Shobha', 'Shreedevi', 'Sreedhara');
my @non_bank_list = ('Muzammil', 'Bindu', 'Chandrakala', 'Vanita');
my $flag = 1;
while ($flag) {
    my $client = Redis::Client->new(host => 'localhost', port => 6379);
    if (check_time()) {
        $flag = 0;
        next;
    }
    my $result = $client->rpop('test_qu');
    if (!$result) {
        write_log("Queue is empty. Sleeping for 5 secs.");
        sleep(5);
    } else {
        write_log("Data recieved - $result");
        my $input_data = decode_json($result);
        if ($input_data->{processingType} eq 'STATEMENT') {
            $manager_id = get_manager_id('bank');
        } elsif ($input_data->{processingType} eq 'Financial Statement' or $input_data->{processingType} eq 'ITR Statement') {
            $manager_id = get_manager_id('non_bank');
        }
        $file = '/home/dhinesh/Credentials/Prohance/serial';
        open FH, $file;
        $serial .= $_ while(<FH>);
        close FH;
        $serial = int($serial) + 1;
        $file = '/home/dhinesh/Credentials/Prohance/serial';
        open F1, ">" . $file;
        binmode F1, ':utf8';
        print F1 $serial;
        close F1;
        write_log("Serial number for this task - $serial");
        write_log("#CREATING_TASK");
        create_task($input_data, $manager_id, $serial);
        write_log("#TASK_CREATION_DONE");
        $serial = '';
    }
}

sub check_time {
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
    if ($hour >= 20) {
        print "Its 08.00PM Hence killing the script";
        return 1;
    } else {
        return 0;
    }
}

sub get_manager_id {
    my $type = shift;
    my $manager = '';
    my $cfg = new Config::Simple('/home/dhinesh/Credentials/Prohance/managerListCfg.ini');
    if ($type eq 'bank') {
        $manager = shift(@bank_list);
        push (@bank_list, $manager);
    } elsif ($type eq 'non_bank') {
        $manager = shift(@non_bank_list);
        push (@non_bank_list, $manager);
    }
    write_log("Manager assigned for this task - $manager");
    my $id = $cfg->param("selector.$manager");
    return $id;
}
=cut
