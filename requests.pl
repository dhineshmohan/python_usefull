#!/usr/bin/perl

use strict;
use WWW::Mechanize;
my $url = 'http://spoonbill.hinagro.com:8080/prohancei/project/config/add';
my $mech = WWW::Mechanize->new();# 'ssl_opts' => { SSL_verify_mode => IO::Socket::SSL::SSL_VERIFY_NONE, 'verify_hostname' => 0 }, 'autocheck' => 0 );
$mech->add_header(
    'User-Agent'      => 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13',
    'Accept'          => '*/*',
    'Accept-Language' => 'en-US',
);
$mech->add_header('Authorization' => 'Basic c3lzYWRtaW46VEdWaUpIbEJTR1ZwY3pVeU1UY3lPVGcwTURVMk1URXlNVFEzTjNCU2IwaGhUbU5GWDBSbFRHbE5hVlJsVWw5VGVVMUNiMHhNWldJa2VVRklaV2x6TlRKd1VtOUlZVTVqUlY5RVpVeHBUV2xVWlZKZlUzbE5RbTlNTVRVME56RXhOVGc0TWpjek1nPT0=');
my $js = "{ \"projectTemplateName\" : \"Bank Statement Template\",\"projectTitle\" : \"ZSZZC223568\",\"projectCode\" : \"BANK-128\",\"projectDescription\" : \"perfios.com\",\"type\" : \"Bank Statement\",\"category\" : \"Bank Statement Processing\",\"startDate\" : \"2019-01-18\",\"endDate\" : \"2019-01-18\",\"estimate\": \"2\",\"manager\" : \"govi\",\"assignees\" : \"govi\",\"customer\" : \"\",\"complexity\" : \"\",\"customAttribute\" : \"[{Applicant Name:PRODUCTION}]\"}";
my $response = $mech->post($url, 'Content-Type' => 'application/json;charset=utf-8',Content => $js);
print $response->decoded_content() . "\n";


my $serial;
my $file;
$file = '/home/dhinesh/Credentials/Prohance/serial';
open FH, $file;
$serial .= $_ while(<FH>);
close FH;

print $serial . "\n";
$serial = int($serial) + 1;
print $serial . "\n";
