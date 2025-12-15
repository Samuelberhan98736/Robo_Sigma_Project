# arm/kinematics.py
import math


class ArmKinematics:
    """
    Forward and inverse kinematics for a simple 4-DOF arm:
    - base rotation
    - shoulder
    - elbow
    - gripper (ignored in position IK)
    """

    def __init__(self, link_lengths: dict):
        """
        :param link_lengths:
            {
              "shoulder": length_cm,
              "elbow": length_cm
            }
        """
        self.L1 = link_lengths["shoulder"]
        self.L2 = link_lengths["elbow"]

    # -------------------------
    # Forward Kinematics (FK)
    # -------------------------

    def forward(self, base_deg, shoulder_deg, elbow_deg):
        """
        Compute (x, y, z) position of end-effector.
        """
        base = math.radians(base_deg)
        shoulder = math.radians(shoulder_deg)
        elbow = math.radians(elbow_deg)

        # Planar position
        r = (
            self.L1 * math.cos(shoulder)
            + self.L2 * math.cos(shoulder + elbow)
        )
        z = (
            self.L1 * math.sin(shoulder)
            + self.L2 * math.sin(shoulder + elbow)
        )

        # Rotate around base
        x = r * math.cos(base)
        y = r * math.sin(base)

        return x, y, z

    # -------------------------
    # Inverse Kinematics (IK)
    # -------------------------

    def inverse(self, x, y, z):
        """
        Solve IK for target (x, y, z).
        Returns (base_deg, shoulder_deg, elbow_deg)
        or None if unreachable.
        """

        # Base angle
        base = math.atan2(y, x)

        # Project to arm plane
        r = math.sqrt(x**2 + y**2)
        d = math.sqrt(r**2 + z**2)

        # Reachability check
        if d > (self.L1 + self.L2) or d < abs(self.L1 - self.L2):
            return None

        # Elbow angle (law of cosines)
        cos_elbow = (d**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        elbow = math.acos(cos_elbow)

        # Shoulder angle
        phi = math.atan2(z, r)
        psi = math.atan2(
            self.L2 * math.sin(elbow),
            self.L1 + self.L2 * math.cos(elbow)
        )
        shoulder = phi - psi

        return (
            math.degrees(base),
            math.degrees(shoulder),
            math.degrees(elbow),
        )
