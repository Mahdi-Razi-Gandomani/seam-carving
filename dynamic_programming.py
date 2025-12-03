import numpy as np


# Dynamic Programming seam finder
class DpMethod:
    def find_vertical_seam(self, energy):
        H, W = energy.shape
        dp = np.full((H, W), float("inf"))
        back = np.full((H, W), -1, dtype=int)
        dp[0, :] = energy[0, :]
        for y in range(1, H):
            for x in range(W):
                best_val = float("inf")
                best_px = -1
                for px in (x - 1, x, x + 1):
                    if 0 <= px < W:
                        val = dp[y - 1, px]
                        if val < best_val:
                            best_val = val
                            best_px = px
                dp[y, x] = best_val + energy[y, x]
                back[y, x] = best_px
        end_x = int(np.argmin(dp[-1, :]))
        seam = [-1] * H
        seam[H - 1] = end_x
        for y in range(H - 1, 0, -1):
            seam[y - 1] = int(back[y, seam[y]])
        return seam

    def find_horizontal_seam(self, energy):
        t = energy.T.copy()
        v_seam = self.find_vertical_seam(t)
        return v_seam
