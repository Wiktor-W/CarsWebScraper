class URL:
    url = "https://www.autotrader.co.uk/car-search?"
    postcode = ""
    price_to = ""
    maximum_mileage = ""
    transmission = ""
    fuel_type = ""
    insuranceGroup = ""
    exclude_writeoff_categories = ""
    year_from = ""
    radius = ""

    def setPostCode(self, postcode):
        self.postcode = postcode
    
    def setPriceTo(self, price):
        self.price_to = price

    def setMaxMileage(self, mileage):
        self.maximum_mileage = mileage
    
    def setTransmission(self, transmission):
        self.transmission = transmission

    def setFuelType(self, fuel):
        self.fuel_type = fuel
    
    def setInsuranceGroup(self, insurance):
        self.insuranceGroup = insurance
    
    def setWriteoff(self, hasCrashed):
        self.exclude_writeoff_categories = hasCrashed

    def setYearProd(self, yearProd):
        self.year_from = yearProd
    
    def setRadius(self, radius):
        self.radius = radius

    def buildUrl(self):
        return url