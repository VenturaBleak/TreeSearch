# solver.py
NEG_INFINITY = float('-inf')
POS_INFINITY = float('inf')

class Solver:
    def alpha_beta(self, node, alpha=NEG_INFINITY, beta=POS_INFINITY, maximizing=True):
        if node.state.is_terminal:
            return node.state.evaluate()
        if maximizing:
            max_eval = NEG_INFINITY
            for child in node.children:
                eval = self.alpha_beta(child, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = POS_INFINITY
            for child in node.children:
                eval = self.alpha_beta(child, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval