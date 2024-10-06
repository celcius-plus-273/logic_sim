class wire:
    
    # member variables
    val = -1 # value on wire defaults to -1 for unassgined
    drive = None
    load = []

    def __init__(self, idx):
        self.idx = idx

    def __str__(self):
        load_output = ''
        return f'Wire #{self.idx}: {self.val}'
