from V2Authorization import V2Authorization



httpHeaders = {"host": {"solarnet"}}
parameters = {}
signedHeaderNames = {}

signingKey = "UF3szxas~=F*C0+9S*E~G{{_"
token = "9;4~LHDQh9E^d||_gRoq"

auth = V2Authorization(token,"GET","https://data.solarnetwork.net/solaruser/api/v1/sec/nodes/meta/321",parameters,
                        httpHeaders, signedHeaderNames)

print(auth.build(signingKey))