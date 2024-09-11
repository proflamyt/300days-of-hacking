

put in your local *dnsmasq.conf*

Format is 

address=/domain name/ IP address
```
address=/#/192.168.200.147
address=/google.com/127.0.0.1
log-queries
```
```
docker pull andyshinn/dnsmasq
docker run --name my-dnsmasq --rm -it -p 0.0.0.0:53:53/udp -v <C:\Users\PREDATOR\Documents\docker-files\dnsmasq.conf>:/etc/dnsmasq.conf andyshinn/dnsmasq
```
