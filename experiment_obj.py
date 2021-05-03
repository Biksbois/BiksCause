

class exp_obj():
    def __init__(self, alpha_val, lambda_val, window_size, head_val, exp_type, exp_size):
        self.alpha_val = alpha_val
        self.lambda_val = lambda_val
        self.window_size = window_size
        self.head_val = head_val
        self.exp_type = exp_type
        self.exp_size = exp_size
        self.nst_keys = self.generate_nst_keys()
    
    def parse_val(self, val):
        return str(val).replace('0.', '')
    
    def one_nst_key(self, a, l):
        return f"nst_a{self.parse_val(a)}_l{self.parse_val(l)}"
    
    def generate_nst_keys(self):
        scores = []
        for a in self.alpha_val:
            for l in self.lambda_val:
                scores.append(self.one_nst_key(a, l))
        
        return scores
