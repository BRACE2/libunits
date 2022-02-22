import anon.atom as anp


def load_hist(s_ref, steps):
    diff = anp.diff(s_ref, axis=0)
    s = anp.array(
        [
            n / stepi * diff[i] + s_ref[i]
            for i, stepi in enumerate(steps)
            for n in range(1, stepi + 1)
        ]
    )
    return s
