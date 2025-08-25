rule SimulatedRansomwareNote
{
    meta:
        description = "Detects simulation ransom note banner"
        author = "Edu Lab"
    strings:
        $a = "THIS_IS_A_SIMULATED_RANSOMWARE_NOTE—EDU_ONLY"
    condition:
        any of them
}
