# SOP & CORS

The same-origin policy is a critical security mechanism that restricts how a document or script loaded by one origin can interact with a resource from another origin.
It helps isolate potentially malicious documents, reducing possible attack vectors.

To clearify this, two URLs have the same origin if the protocol, port (if specified), and host are the same for both, URLs that doesn't meet this required specifications would be restricted from sharing resources. that is, the response from another domain would be inaccessible 
from a browser with diffrent domain.
To reinstate this, request made from a diffrent domain would be sent but the response would be inaccessible. Also, this is only applicable in the browser and this wont prevent attacks like cross-site request forgery (CSRF).

Tricking a visitor to your website and making them make a request to another diffrent domain would be successful but the response from this domains would be inaccessible, which still leaves room for DDOS and making a request to the target website 
on behalf of the victim


# CORS

Cross-Origin Resource Sharing (CORS) is an HTTP-header based mechanism that allows a server to indicate any origins (domain, scheme, or port) other than its own from which a browser should permit loading resources.

There are cases where legitimate websites wants to access their resources across diffrent domains. In a situation whereby the backend application is hosted on a diffrent sub domain or a diffrent domain entitrely and the frontend application needs to access these resources .
This normally would be impossible due to SOP, But there are laxes in these restrictions cause of situations like these.





refrences: https://security.stackexchange.com/questions/145013/when-does-the-same-origin-policy-prevent-a-request-from-being-sent#:~:text=implementing%20CSRF%20tokens.-,Are%20there%20any%20cases%20where%20SOP%20prevents%20the%20request%20from,origin%20resource%20sharing%20(CORS).
