The combination of `Vless` and `Reality` is the most powerful strategy nowadays to disguise the TCP traffic and it's been widely applied across the world for VPN and proxy techniques to break through the networking blockade since it provides the best privacy on hiding your proxy nodes.
<img src="/assets/mermaid-diagram.png">

This diagram shows the whole process very clearly.

## Step 1 "TLS" Handshake

That's the most fantastic and innovative method created by Reality.

Traditionally, other protocols for proxy normally requires nodes owners to register certificates on their own with some cheap certificates.

1. Then GFW will easily notice such suspicious sites by observing these sites and look up in the Certificate Transparency Logs, discovering such newly registered domains with suddenly huge amount of cross-country traffics. Soon the TLS with the domain name will be cut down directly, or maybe it's the IP address of it or the IP + port.

2. Though TLSv1.3 provides the encryption of certificates, probes can still get the certificates by directly sending TLS ClientHello to it. Also, probes will receive some normal error messages of proxy protocols thus causing more blockings.

Then, people of Xray community provides a brand new method called Reality to solve the problem. They no longer apply for the own certificates by their own. Instead, they use them of big companies like Apple, Microsoft, Sony, etc.

OK, let's start introducing some details of Reality protocol, which is mainly for the initial TLS handshake and establish a encryption tunnel. (Wish I can make it clear)

The Reality, is intended to solve the problem:

**How to directly borrow the certificates from big companies to disguise while still managing to complete the TLS handshake without certificate's private key, and prevent probings to investigate it's a proxy server, not the real, let's say, `apple.com`?**

1. Client Hello. (Making the server to trust the identity of Client)

Note that we talk about the TLSv1.3 here, where the certificate will be encrypted first and then be sent along with ServerHello.

Also, you should distinguish the public keys of **Reality** and **TLS** handshake.

Here, just like normal one, the client sends the SNI (disguised) and a temporary public key to the proxy server.

(Here, the public key from the client will take participate in two places: construction of $K_{auch}$ and normal TLS.)

**Attention**! Since we already know the public key of Reality when configuration, so the $K_{auth}$ can be computed in the Client side by server's reality public key and the local TLS private key. It will be used to encrypt and authenticate to get the 32-byte session-id field in `ClientHello` package. (The inputs are the the admission messages of Reality like the short-id, timestamp, client version, a reserved byte; Then outputs will be two 16-byte fields, one for encryption, another for authentication, making sure the encrypted 16 bytes wasn't be modified by others using the $k_{auth}$ key)

2. After server receiving ClientHello, it would: (response is for letting client trust you are the proxy server)

	1. The server constructs the $K_{auth}$ by its Reality private key and Client's TLS Public key. Since they both use the X25519 algorithm.
	
	2. Look at the SNI, which should be plaintext. (Maybe encrypt it will be safer incase the GFW checks the IP / domain name matching. But now we assume it only detect by probes). 
		
		Note that here it has not decrypted the field. But it would first send the copy the TLS Client Hello to the cover site(the one in SNI). `session-id` field is the legacy so normally it would return as usual.
		
		Since it's the raw copy, the cover site would close the connection if it's malformed or things like that.
	
		The reason why the server does this step no matter who comes is in the next point, the two cases.

	3. The server checks the `session-id` field. 
		- If it's alright, then the later TLS handshake will go in the Reality way. 
		
			Here's the interesting thing: **we make the response resemble the cover site**.
			
			This is for preventing the **observation** of GFW. 
			
			1. There will be some plaintext in the server response, including its negotiated parameters.
			
			2. Also, the lengths and arrangement of encrypted TLS records. So basically, you should make the encrypted Reality certificate (will talk about later) as long as the cover site's, so it normally use padding.
		
		- But if it's not right, here the most important thing: the server will act as a relay of the cover site, sending its Server Response of TLS directly back to the probe, so that it will look just the authenticate, the real cover site, like `apple.com` because the certificate is all correct. 
		
			Therefore, there's no way distinguishing it with normal HTTPS traffic if you put the target port at 443.
			
			So this is for **preventing probes.**

	4. Then the server should build its server response field now.  In case others can know it's not the normal TLS response, only encrypted fields will be modified so that nobody will know except the client. 
	
		1. Use Ed25519 algorithm to generate a new public / private key pair, which is used to replace the ones of certificate's.
		
		2. Then as what the server response normally does, it needs to prove to the client I am the real server you want. So originally it should prove that it has the right certificate.
		
		3. Write the "Hash" of the public key of certificate authenticated by the $K_{auth}$ in the field `certificate’s signature-value`. 
		
		4. Then in case others directly copy the above public keys and the hash, `CertificateVerify` use the private key to sign the handshake history so far.
		
		Finally, the response is constructed well. And in others' eyes, it looks just like the normal one of `apple.com`.
		
	5. The client received the server response. Using its $K_{auth}$ to compute the expected hash of public key from TLS, then compare with `CertificateVerify`.
	
	   After confirming, the client can trust the server because there won't be an impersonator who can compute the write `CertificateVerify` without $K_{auth}$ even if it changes the public key and hash both.
	   
	Till now, TLS handshake completes. (maybe some details left, but I think almost here)

## Step 2 Vless

The Reality is mainly for disguise. Though you can use the `short-id` to recognize the user. But there are many other things todo and it will change the Reality protocol itself.

So based on the requirement of managing users from subscriptions, here comes the `Vless` protocol. 

Here's what ChatGPT tells me about its header.

| Field                  | Size     | Purpose                                       |
| ---------------------- | -------- | --------------------------------------------- |
| Version                | 1 byte   | Protocol version                              |
| UUID                   | 16 bytes | User credential                               |
| Addons length + addons | Variable | Optional settings, including flow information |
| Command                | 1 byte   | TCP, UDP, etc.                                |
| Port                   | 2 bytes  | Destination port                              |
| Address type + address | Variable | Destination IPv4, IPv6, or hostname           |
| Payload                | Variable | Data to forward                               |

It stands on top of TCP.

The arriving orders would be ensured by TCP so order has nothing to do with Vless. It only needs to tell the proxy server some identity information and following steps with real addresses and ports.

Then the proxy application will paste the data inside TCP into a new buffer. When the data from the start point of buffer all present, then new TCP packets will be constructed by OS automatically, sent to your destination, which has been decided after getting the Vless header.

So it's like a stream.

The Vless header will be sent only once and only data inside TCP would be copied.

So why do we use Vless exactly?

1. You can let multiple users share one Reality short-id and removing each of them keeps Reality intact.

2. The account mapping also connects users to policies, logs, and traffic statistics with Vless enabled.