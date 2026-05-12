import urllib.request, json, urllib.error

def api(url, data=None, token=None):
    h = {'Content-Type':'application/json'}
    if token: h['Authorization']='Bearer '+token
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=h)
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

B = 'http://127.0.0.1:5000/api'

r = api(B+'/auth/register', {'name':'Sunil Farmer','email':'sunil@test.com','password':'test123','role':'farmer','farm_location':'Pune, Maharashtra','farming_type':'Organic','crops_category':'Vegetables,Fruits','upi_id':'sunil@upi','referral_code':'AHFARMER1'})
print('FARMER:', r.get('message',''), '| ref:', r.get('user',{}).get('referral_code'))

r2 = api(B+'/auth/register', {'name':'Anjali Customer','email':'anjali@test.com','password':'test123','role':'customer','payment_method':'upi'})
print('CUSTOMER:', r2.get('message',''))

r3 = api(B+'/auth/register', {'name':'Raj Delivery','email':'raj@test.com','password':'test123','role':'delivery','vehicle_type':'Bike','license_number':'MH12CD5678'})
print('DELIVERY:', r3.get('message',''), '| vehicle:', r3.get('user',{}).get('vehicle_type'))

r4 = api(B+'/auth/register', {'name':'Bad Ref','email':'bad@test.com','password':'test123','role':'customer','referral_code':'INVALID99'})
print('BAD REF:', r4.get('error',''))

print('PRODUCTS:', len(api(B+'/products/')['products']), 'items seeded')
