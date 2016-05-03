output "cname" {
    value = "${aws_route53_record.db_cname.fqdn}"
    value = "${aws_route53_record.traffic_cname.fqdn}"
    value = "${aws_route53_record.web_cname.fqdn}"
    value = "${aws_route53_record.aux_cname.fqdn}"
}
