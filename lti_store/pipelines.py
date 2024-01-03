from itertools import chain
from typing import Dict

from openedx_filters import PipelineStep

from lti_store.models import ExternalLtiConfiguration
from lti_store.apps import LtiStoreConfig


class GetLtiConfigurations(PipelineStep):
    """
    Get all available LTI configurations

    Example usage:

    Add the following configurations to your configuration file:

        OPEN_EDX_FILTERS_CONFIG = {
            "org.openedx.xblock.lti_consumer.configuration.listed.v1": {
                "fail_silently": false,
                "pipeline": [
                    "lti_store.pipelines.GetLtiConfigurations"
                ]
            }
        }
    """

    PLUGIN_PREFIX = LtiStoreConfig.name

    def run_filter(
        self, context: Dict, config_id: str, configurations: Dict, *args, **kwargs
    ):  # pylint: disable=arguments-differ, unused-argument
        config = {}
        if config_id:
            _slug = config_id.split(":")[1]
            try:
                config_object = ExternalLtiConfiguration.objects.get(slug=_slug)
                config = {
                    f"{self.PLUGIN_PREFIX}:{config_object.slug}": full_model_to_dict(
                        config_object
                    )
                }
            except ExternalLtiConfiguration.DoesNotExist:
                config = {}
        else:
            config_objs = ExternalLtiConfiguration.objects.all()
            config = {
                f"{self.PLUGIN_PREFIX}:{c.slug}": full_model_to_dict(c) for c in config_objs
            }

        configurations.update(config)
        return {
            "configurations": configurations,
            "config_id": config_id,
            "context": context,
        }


def full_model_to_dict(instance):
    """ Converts a django model instance to a dict, including all fields. """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    return data