#!/usr/bin/perl
use strict;
use JSON;
use WWW::Mechanize;
use POSIX qw(strftime);


my $url = 'http://spoonbill.hinagro.com:8080/prohancei/project/config/add';
my $mech = WWW::Mechanize->new();
$mech->add_header(
    'User-Agent'      => 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13',
    'Accept'          => '*/*',
    'Accept-Language' => 'en-US',
    'Authorization'   => 'Basic c3lzYWRtaW46VEdWaUpIbEJTR1ZwY3pVeU1UY3lPVGcwTURVMk1URXlNVFEzTjNCU2IwaGhUbU5GWDBSbFRHbE5hVlJsVWw5VGVVMUNiMHhNWldJa2VVRklaV2x6TlRKd1VtOUlZVTVqUlY5RVpVeHBUV2xVWlZKZlUzbE5RbTlNTVRVME56RXhOVGc0TWpjek1nPT0=',
);
my $data = $ARGV[0];
my @arr = split('\n', $data);
create_task($arr[0], $arr[1], $arr[2]);
write_log("#END_TASK_CREATION");

sub create_task {
    my $input_data = shift;
    my $manager_id = shift;
    my $serial = shift;
    write_log($input_data);
    $input_data = decode_json($input_data);
    my $req_data = get_json($input_data);
    write_serial($serial);
    my $pro_code = $req_data->{serial_pref} . $serial;
    my $date = strftime "%Y-%m-%d", localtime;
    my $js = "{ \"projectTemplateName\" : \"$req_data->{process_template}\",\"projectTitle\" : \"$input_data->{perfiosTransactionId}\",\"projectCode\" : \"$pro_code\",\"projectDescription\" : \"$input_data->{downloadUrl}\",\"type\" : \"$req_data->{process_type}\",\"category\" : \"$req_data->{process_catagory}\",\"startDate\" : \"$date\",\"endDate\" : \"$date\",\"estimate\": \"2\",\"manager\" : \"$manager_id\",\"assignees\" : \"$manager_id\",\"customer\" : \"\",\"complexity\" : \"\",\"customAttribute\" : \"[{Applicant Name:$input_data->{environment}}]\"}";
    write_log("JSON passed to the api - $js");
    my $response = $mech->post($url, 'Content-Type' => 'application/json;charset=utf-8',Content => $js);
    my $response_message = decode_json($response->decoded_content());
    if ($response_message->{operatonStatus} eq 'SUCCESS') {
        write_log("Task created successfully. $response_message->{reason}");
    } elsif ($response_message->{operatonStatus} eq 'FAILURE') {
        write_log("Task creation failed. Reason - $response_message->{reason}");
    }
}

sub get_json {
    my $input_data = shift;
    my $process_json = '{"bank_statement" : {"process_template" : "Bank Statement Template", "process_type" : "Bank Statement", "process_catagory" : "Bank Statement Processing", "serial_pref" : "BANK"}, "final_statement" : {"process_template" : "Financial Statement Template", "process_type" : "Financial Statement", "process_catagory" : "Financial Statement Processing", "serial_pref" : "FIN"}, "itr_statement" : {"process_template" : "ITR Statement Template", "process_type" : "Financial Statement", "process_catagory" : "Financial Statement Processing", "serial_pref" : "ITR"} }';
    $process_json = decode_json($process_json);
    my $req_json;
    if ($input_data->{processingType} eq 'STATEMENT') {
        $req_json = $process_json->{bank_statement};
    } elsif ($input_data->{processingType} eq 'Financial Statement') {
        $req_json = $process_json->{final_statement};
    } elsif ($input_data->{processingType} eq 'ITR Statement') {
        $req_json = $process_json->{itr_statement};
    }
    write_log("Required JSON set");
    return $req_json;
}

sub write_log {
    my $msg = shift;
    $msg .= "\n";
    my $message = 'KFetcher:' . time() . ': ' . $msg; 
    my $date = strftime "%Y-%m-%d", localtime;
    my $file_name = '/home/dhinesh/Prohance/Logs/' . 'prohance_logs_' . $date . '.log';
    $file_name =~ s/-/_/gi;
    open F1, ">>" . $file_name;
    binmode F1, ':utf8';
    print F1 $message;
    close F1;
}

sub write_serial {
    my $content = shift;
    my $file = '/home/dhinesh/Credentials/Prohance/serial';
    open F2, ">" . $file;
    binmode F2, ':utf8';
    print F2 $content;
    close F2;
}
