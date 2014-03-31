# Introducing a class that only handles the service, not the
# various HTTP magic.  The present class is essentially a mockup
# that communicates with the associated test.  Later it will be
# replaced by a proper class with it own tests, and the test
# system will use its own mock.  But all in its own good time.


class SmsService:

    def get_service_configuration(self):
        # XXX Payload code missing        
        return {
            "mom_instance_id" : "tnn",
            "supported_billing" : [ "FREE", "SUBSCRIPTION" ],
            "supported_int_prefixes" : [ "+46", "+47" ],
            "supports_mms" : False,
            "supports_delivery_notification" : True,
            "copy_event_on_submit" : False
        }


    def update_user_provisioning(self, uuid, facility, provision_status):
        # XXX Payload code missing
        failure = False
        if (not failure):
            return  {}
        return {
            "uuid" : uuid,
            "success" : False,
            "description" : "Invalid subscriber"
            }


    def submit_sms(self, recipient, originator, text, billing, uuid, delivery_notification_requested):
        # XXX Payload code missing

        #        print "sending to "
        #        print recipient
        
        failure = False
        if (not failure):
            return  {}
        return {
            "success" : False,
            "uuid" : uuid,
            "description" : "Invalid recipient"
            }


    def get_next_event(self):
        # These are the three types of events we are expected to
        # send to the recipients.
        provisioned_subscriber_event = {
            "uuid" : "1a86ac57-ef05-4e72-9c36-6e10526f5f2c",
            "receiptId" : "1a86ac57-ef05-4e72-9c36-6e10526f5f2c/5678",
            "link" : {
                "href" : "ack?receiptId=1a86ac57-ef05-4e72-9c36-6e10526f5f2c/5678",
                "rel" : "ack"
                },
                "sms_event" : {
                    "is_incoming" : True,
                    "timestamp" : 1394625725116,
                    "sms" : {
                        "recipient" : [ "+4792420683" ],
                        "originator" : "+4795789351",
                        "text" : "Lorem ipsum"
                    }
                }
        }

        incoming_message_event = {
            "uuid" : "ce3c670a-43f2-4a8d-b8db-66fb11ed9092",
            "receiptId" : "ce3c670a-43f2-4a8d-b8db-66fb11ed9092/1234",
            "link" : {
                "href" : "ack?receiptId=ce3c670a-43f2-4a8d-b8db-66fb11ed9092/1234",
                "rel" : "ack"
                },
                "sms_event" : {
                    "is_incoming" : False,
                    "timestamp" : 1394625725127,
                    "sms" : {
                        "recipient" : [ "+4795789351" ],
                        "originator" : "+4792420683",
                        "text" : "Lorem ipsum"
                    }
                }
        }

        deprovisioned_subscriber_event = {
            "uuid" : "062411dd-dd5b-4ae9-b2fa-48a698b70ee6",
            "receiptId" : "062411dd-dd5b-4ae9-b2fa-48a698b70ee6/9045",
            "link" : {
                "href" : "ack?receiptId=062411dd-dd5b-4ae9-b2fa-48a698b70ee6/9045",
                "rel" : "ack"
                },
                "provision_event" : {
                    "timestamp" : 1394625725128,
                    "subscriber" : "+4792420683",
                    "provision_status" : "DELETE",
                    "facility" : [ "SMS", "MMS" ]
                }
        }
        
        no_event = {}
        
        return no_event

    def is_subscriber_hosted_with_this_provider(self, subscriber):
        return {
            "msisdn" : subscriber,
            "served_by_provider" : True
         }


    def get_subscription(self, subscriber):
        return {
            "msisdn" : "+4792420683",
            "user_name" : "Arne Georg Gleditsch",
            "brand" : "telenor"
            }


    def get_subscriber_info(self, subscriber):
        return {
            "msisdn" : "+4792420683",
            "user_name" : "Arne Georg Gleditsch",
            "brand" : "telenor"
            }
