# Notes

## Query Types

<https://github.com/TechnitiumSoftware/TechnitiumLibrary/blob/750bda6a8346cbfdd8d3d62a6944961ba88ec58f/TechnitiumLibrary.Net/Dns/ResourceRecords/DnsResourceRecord.cs#L27-L128>

```
Unknown = 0
A = 1
NS = 2
MD = 3
MF = 4
CNAME = 5
SOA = 6
MB = 7
MG = 8
MR = 9
NULL = 10
WKS = 11
PTR = 12
HINFO = 13
MINFO = 14
MX = 15
TXT = 16
RP = 17
AFSDB = 18
X25 = 19
ISDN = 20
RT = 21
NSAP = 22
NSAP_PTR = 23
SIG = 24
KEY = 25
PX = 26
GPOS = 27
AAAA = 28
LOC = 29
NXT = 30
EID = 31
NIMLOC = 32
SRV = 33
ATMA = 34
NAPTR = 35
KX = 36
CERT = 37
A6 = 38
DNAME = 39
SINK = 40
OPT = 41
APL = 42
DS = 43
SSHFP = 44
IPSECKEY = 45
RRSIG = 46
NSEC = 47
DNSKEY = 48
DHCID = 49
NSEC3 = 50
NSEC3PARAM = 51
TLSA = 52
SMIMEA = 53
HIP = 55
NINFO = 56
RKEY = 57
TALINK = 58
CDS = 59
CDNSKEY = 60
OPENPGPKEY = 61
CSYNC = 62
ZONEMD = 63
SVCB = 64
HTTPS = 65
SPF = 99
UINFO = 100
UID = 101
GID = 102
UNSPEC = 103
NID = 104
L32 = 105
L64 = 106
LP = 107
EUI48 = 108
EUI64 = 109
NXNAME = 128
TKEY = 249
TSIG = 250
IXFR = 251
AXFR = 252
MAILB = 253
MAILA = 254
ANY = 255
URI = 256
CAA = 257
AVC = 258
DOA = 259
AMTRELAY = 260
RESINFO = 261
WALLET = 262
CLA = 263
IPN = 264
TA = 32768
DLV = 32769
ANAME = 65280
FWD = 65281
APP = 65282
ALIAS = 65357
```

## Response Types

<https://github.com/TechnitiumSoftware/DnsServer/blob/59b03b5bfe16114c467b1c9130b6a34b35bec9cc/DnsServerCore.ApplicationCommon/IDnsQueryLogger.cs#L27-L28>

```
1: Authoritative
2: Recursive
3: Cached
4: Blocked
5: UpstreamBlocked
6: CacheBlocked
7: Dropped
```

## Response Codes

<https://github.com/TechnitiumSoftware/TechnitiumLibrary/blob/750bda6a8346cbfdd8d3d62a6944961ba88ec58f/TechnitiumLibrary.Net/Dns/DnsDatagram.cs#L46>

```
0: NoError
1: FormatError
2: ServerFailure
3: NxDomain
4: NotImplemented
5: Refused
6: YXDomain
7: YXRRSet
8: NXRRSet
9: NotAuth
10: NotZone
16: BADVERS
17: BADCOOKIE
```

Everything other than 0 is an error of some kind.

# Grafana

## Chart

```sql
SELECT
    CASE response_type
        WHEN 1 THEN 'Authoritative'
        WHEN 2 THEN 'Recursive'
        WHEN 3 THEN 'Cached'
        WHEN 4 THEN 'Blocked'
        WHEN 5 THEN 'Upstream Blocked'
        WHEN 6 THEN 'Cache Blocked'
        WHEN 7 THEN 'Dropped'
    END as response_type_name,
UNIX_TIMESTAMP(DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i:00')) AS time, COUNT(*) AS Responses
FROM dns_logs
WHERE $__timeFilter(timestamp)
GROUP BY time, response_type
ORDER BY time ASC;
```

Add a `Multi-frame time series` transformation.

## Top Allowed Domains

```sql
SELECT qname as Domain, COUNT(*) AS Hits
FROM dns_logs
WHERE $__timeFilter(timestamp)
/* Only get requests that were successfully Authoritative, Recursive, or Cached */
AND (response_type = 1 OR response_type = 2 OR response_type = 3)
/* Only show requests that returned a response */
AND rcode = 0
GROUP BY Domain
ORDER BY Hits DESC
LIMIT 20;
```

## Top Blocked Domains

```sql
SELECT qname as Domain, COUNT(*) AS Hits
FROM dns_logs
WHERE $__timeFilter(timestamp)
/* Only get requests that were blocked */
AND (response_type = 4 OR response_type = 5 OR response_type = 6)
GROUP BY Domain
ORDER BY Hits DESC
LIMIT 20;
```

## Response Type Breakdown

```sql
SELECT
    CASE response_type
        WHEN 1 THEN 'Authoritative'
        WHEN 2 THEN 'Recursive'
        WHEN 3 THEN 'Cached'
        WHEN 4 THEN 'Blocked'
        WHEN 5 THEN 'Upstream Blocked'
        WHEN 6 THEN 'Cache Blocked'
        WHEN 7 THEN 'Dropped'
    END
AS 'Response Type', COUNT(*) AS Quantity
FROM dns_logs
WHERE $__timeFilter(timestamp)
GROUP BY response_type
ORDER BY Quantity DESC;
```

## Query Type Breakdown

```sql
SELECT
    CASE qtype
        WHEN 0 THEN 'Unknown'
        WHEN 1 THEN 'A'
        WHEN 2 THEN 'NS'
        WHEN 3 THEN 'MD'
        WHEN 4 THEN 'MF'
        WHEN 5 THEN 'CNAME'
        WHEN 6 THEN 'SOA'
        WHEN 7 THEN 'MB'
        WHEN 8 THEN 'MG'
        WHEN 9 THEN 'MR'
        WHEN 10 THEN 'NULL'
        WHEN 11 THEN 'WKS'
        WHEN 12 THEN 'PTR'
        WHEN 13 THEN 'HINFO'
        WHEN 14 THEN 'MINFO'
        WHEN 15 THEN 'MX'
        WHEN 16 THEN 'TXT'
        WHEN 17 THEN 'RP'
        WHEN 18 THEN 'AFSDB'
        WHEN 19 THEN 'X25'
        WHEN 20 THEN 'ISDN'
        WHEN 21 THEN 'RT'
        WHEN 22 THEN 'NSAP'
        WHEN 23 THEN 'NSAP_PTR'
        WHEN 24 THEN 'SIG'
        WHEN 25 THEN 'KEY'
        WHEN 26 THEN 'PX'
        WHEN 27 THEN 'GPOS'
        WHEN 28 THEN 'AAAA'
        WHEN 29 THEN 'LOC'
        WHEN 30 THEN 'NXT'
        WHEN 31 THEN 'EID'
        WHEN 32 THEN 'NIMLOC'
        WHEN 33 THEN 'SRV'
        WHEN 34 THEN 'ATMA'
        WHEN 35 THEN 'NAPTR'
        WHEN 36 THEN 'KX'
        WHEN 37 THEN 'CERT'
        WHEN 38 THEN 'A6'
        WHEN 39 THEN 'DNAME'
        WHEN 40 THEN 'SINK'
        WHEN 41 THEN 'OPT'
        WHEN 42 THEN 'APL'
        WHEN 43 THEN 'DS'
        WHEN 44 THEN 'SSHFP'
        WHEN 45 THEN 'IPSECKEY'
        WHEN 46 THEN 'RRSIG'
        WHEN 47 THEN 'NSEC'
        WHEN 48 THEN 'DNSKEY'
        WHEN 49 THEN 'DHCID'
        WHEN 50 THEN 'NSEC3'
        WHEN 51 THEN 'NSEC3PARAM'
        WHEN 52 THEN 'TLSA'
        WHEN 53 THEN 'SMIMEA'
        WHEN 55 THEN 'HIP'
        WHEN 56 THEN 'NINFO'
        WHEN 57 THEN 'RKEY'
        WHEN 58 THEN 'TALINK'
        WHEN 59 THEN 'CDS'
        WHEN 60 THEN 'CDNSKEY'
        WHEN 61 THEN 'OPENPGPKEY'
        WHEN 62 THEN 'CSYNC'
        WHEN 63 THEN 'ZONEMD'
        WHEN 64 THEN 'SVCB'
        WHEN 65 THEN 'HTTPS'
        WHEN 99 THEN 'SPF'
        WHEN 100 THEN 'UINFO'
        WHEN 101 THEN 'UID'
        WHEN 102 THEN 'GID'
        WHEN 103 THEN 'UNSPEC'
        WHEN 104 THEN 'NID'
        WHEN 105 THEN 'L32'
        WHEN 106 THEN 'L64'
        WHEN 107 THEN 'LP'
        WHEN 108 THEN 'EUI48'
        WHEN 109 THEN 'EUI64'
        WHEN 128 THEN 'NXNAME'
        WHEN 249 THEN 'TKEY'
        WHEN 250 THEN 'TSIG'
        WHEN 251 THEN 'IXFR'
        WHEN 252 THEN 'AXFR'
        WHEN 253 THEN 'MAILB'
        WHEN 254 THEN 'MAILA'
        WHEN 255 THEN 'ANY'
        WHEN 256 THEN 'URI'
        WHEN 257 THEN 'CAA'
        WHEN 258 THEN 'AVC'
        WHEN 259 THEN 'DOA'
        WHEN 260 THEN 'AMTRELAY'
        WHEN 261 THEN 'RESINFO'
        WHEN 262 THEN 'WALLET'
        WHEN 263 THEN 'CLA'
        WHEN 264 THEN 'IPN'
        WHEN 32768 THEN 'TA'
        WHEN 32769 THEN 'DLV'
        WHEN 65280 THEN 'ANAME'
        WHEN 65281 THEN 'FWD'
        WHEN 65282 THEN 'APP'
        WHEN 65357 THEN 'ALIAS'
    END
AS 'Query Type', COUNT(*) AS Quantity
FROM dns_logs
WHERE $__timeFilter(timestamp)
GROUP BY qtype
ORDER BY Quantity DESC;
```

## Response Time

```sql
SELECT response_rtt
FROM dns_logs
WHERE $__timeFilter(timestamp)
AND response_rtt IS NOT NULL
```

## Query Log

```sql
SELECT qname as Domain,
    CASE response_type
        WHEN 1 THEN 'Authoritative'
        WHEN 2 THEN 'Recursive'
        WHEN 3 THEN 'Cached'
        WHEN 4 THEN 'Blocked'
        WHEN 5 THEN 'Upstream Blocked'
        WHEN 6 THEN 'Cache Blocked'
        WHEN 7 THEN 'Dropped'
    END as "Response Type",
    CASE qtype
        WHEN 0 THEN 'Unknown'
        WHEN 1 THEN 'A'
        WHEN 2 THEN 'NS'
        WHEN 3 THEN 'MD'
        WHEN 4 THEN 'MF'
        WHEN 5 THEN 'CNAME'
        WHEN 6 THEN 'SOA'
        WHEN 7 THEN 'MB'
        WHEN 8 THEN 'MG'
        WHEN 9 THEN 'MR'
        WHEN 10 THEN 'NULL'
        WHEN 11 THEN 'WKS'
        WHEN 12 THEN 'PTR'
        WHEN 13 THEN 'HINFO'
        WHEN 14 THEN 'MINFO'
        WHEN 15 THEN 'MX'
        WHEN 16 THEN 'TXT'
        WHEN 17 THEN 'RP'
        WHEN 18 THEN 'AFSDB'
        WHEN 19 THEN 'X25'
        WHEN 20 THEN 'ISDN'
        WHEN 21 THEN 'RT'
        WHEN 22 THEN 'NSAP'
        WHEN 23 THEN 'NSAP_PTR'
        WHEN 24 THEN 'SIG'
        WHEN 25 THEN 'KEY'
        WHEN 26 THEN 'PX'
        WHEN 27 THEN 'GPOS'
        WHEN 28 THEN 'AAAA'
        WHEN 29 THEN 'LOC'
        WHEN 30 THEN 'NXT'
        WHEN 31 THEN 'EID'
        WHEN 32 THEN 'NIMLOC'
        WHEN 33 THEN 'SRV'
        WHEN 34 THEN 'ATMA'
        WHEN 35 THEN 'NAPTR'
        WHEN 36 THEN 'KX'
        WHEN 37 THEN 'CERT'
        WHEN 38 THEN 'A6'
        WHEN 39 THEN 'DNAME'
        WHEN 40 THEN 'SINK'
        WHEN 41 THEN 'OPT'
        WHEN 42 THEN 'APL'
        WHEN 43 THEN 'DS'
        WHEN 44 THEN 'SSHFP'
        WHEN 45 THEN 'IPSECKEY'
        WHEN 46 THEN 'RRSIG'
        WHEN 47 THEN 'NSEC'
        WHEN 48 THEN 'DNSKEY'
        WHEN 49 THEN 'DHCID'
        WHEN 50 THEN 'NSEC3'
        WHEN 51 THEN 'NSEC3PARAM'
        WHEN 52 THEN 'TLSA'
        WHEN 53 THEN 'SMIMEA'
        WHEN 55 THEN 'HIP'
        WHEN 56 THEN 'NINFO'
        WHEN 57 THEN 'RKEY'
        WHEN 58 THEN 'TALINK'
        WHEN 59 THEN 'CDS'
        WHEN 60 THEN 'CDNSKEY'
        WHEN 61 THEN 'OPENPGPKEY'
        WHEN 62 THEN 'CSYNC'
        WHEN 63 THEN 'ZONEMD'
        WHEN 64 THEN 'SVCB'
        WHEN 65 THEN 'HTTPS'
        WHEN 99 THEN 'SPF'
        WHEN 100 THEN 'UINFO'
        WHEN 101 THEN 'UID'
        WHEN 102 THEN 'GID'
        WHEN 103 THEN 'UNSPEC'
        WHEN 104 THEN 'NID'
        WHEN 105 THEN 'L32'
        WHEN 106 THEN 'L64'
        WHEN 107 THEN 'LP'
        WHEN 108 THEN 'EUI48'
        WHEN 109 THEN 'EUI64'
        WHEN 128 THEN 'NXNAME'
        WHEN 249 THEN 'TKEY'
        WHEN 250 THEN 'TSIG'
        WHEN 251 THEN 'IXFR'
        WHEN 252 THEN 'AXFR'
        WHEN 253 THEN 'MAILB'
        WHEN 254 THEN 'MAILA'
        WHEN 255 THEN 'ANY'
        WHEN 256 THEN 'URI'
        WHEN 257 THEN 'CAA'
        WHEN 258 THEN 'AVC'
        WHEN 259 THEN 'DOA'
        WHEN 260 THEN 'AMTRELAY'
        WHEN 261 THEN 'RESINFO'
        WHEN 262 THEN 'WALLET'
        WHEN 263 THEN 'CLA'
        WHEN 264 THEN 'IPN'
        WHEN 32768 THEN 'TA'
        WHEN 32769 THEN 'DLV'
        WHEN 65280 THEN 'ANAME'
        WHEN 65281 THEN 'FWD'
        WHEN 65282 THEN 'APP'
        WHEN 65357 THEN 'ALIAS'
    END as "Query Type",
    answer as Answer,
    DATE_FORMAT(timestamp, '%H:%i:%s') AS Time
FROM dns_logs
WHERE $__timeFilter(timestamp)
ORDER BY timestamp DESC
LIMIT 50
```
