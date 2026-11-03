import grpc
from config import ConfigTinkoff
from tinkoff.invest.grpc import (
    instruments_pb2,
    instruments_pb2_grpc,
)

config_tinkoff = ConfigTinkoff().model_dump()
token = config_tinkoff.get("api_token").get_secret_value()
sandbox_service_endpoint = config_tinkoff.get("sandbox_service_endpoint")


def main() -> None:
    with open("certs/RussianTrustedRootCA.pem", "rb") as cert_file:
        root_certificates = cert_file.read()
    with grpc.secure_channel(
        target=sandbox_service_endpoint,
        credentials=grpc.ssl_channel_credentials(root_certificates=root_certificates),
    ) as channel:
        print("Channel created successfully.")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
            print("Connection established successfully.")
            instruments = instruments_pb2_grpc.InstrumentsServiceStub(channel)
            response = instruments.Shares(
                instruments_pb2.InstrumentsRequest(),
                metadata=(("authorization", f"Bearer {token}"),),
                timeout=5,
            )
            print("Response received:", response)
        except grpc.FutureTimeoutError:
            print("Connection timed out.")
        except grpc.RpcError as error:
            print(f"gRPC code: {error.code()}")
            print(f"gRPC details: {error.details()}")


if __name__ == "__main__":
    main()
