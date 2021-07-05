class Order:

    def __init__(self,ord_num,ord_import,ord_advance,ord_date,cust_id,agent_code,description):
        self.ord_num = ord_num
        self.ord_import = ord_import
        self.ord_advance = ord_advance
        self.ord_date = ord_date
        self.cust_id=cust_id
        self.agent_code=agent_code
        self.description=description

    def OrderDetail(self):
        return {'num_ord':self.ord_num,'importOrder':self.ord_import,'advance_ord':self.ord_advance,'ordDate':self.ord_date,'Cust_id':self.cust_id,'Description':self.ord_num}
