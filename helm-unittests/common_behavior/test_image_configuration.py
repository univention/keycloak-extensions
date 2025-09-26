# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.best_practice.image_configuration import \
    ImageConfiguration


class TestImageConfiguration(ImageConfiguration):
    def adjust_values(self, values: dict):
        if "image" in values:
            image = values.pop("image")
            values["handler"] = {"image": image}
            values["proxy"] = {"image": image}
        return values
