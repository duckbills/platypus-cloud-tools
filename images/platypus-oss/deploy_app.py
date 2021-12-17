import argparse
import json
import os
from collections import namedtuple
from queue import Queue
from subprocess import Popen, PIPE
from threading import Thread


def main():
    parser = argparse.ArgumentParser(description='Deploy Single Node Platypus')
    parser.add_argument(dest='platypus_data_path', type=str, help='path to platypus data files')
    parser.add_argument(dest='boto_cfg_file_path', type=str, help='path to boto config')
    parser.add_argument(dest='bucket_name', type=str, help='amazon s3 bucket name where indexes will be backed up')
    parser.add_argument(dest='service_name', type=str, help='service namespace on amazon s3',
                        default='platypus-single-node')
    parser.add_argument(dest='restore_state', type=str, default='no', help='Restore a previously created deployment')

    args = parser.parse_args()
    server_proc_manager = ServerProcManager(args)
    server_proc_manager.start()


class ServerProcManager:
    ServerType = namedtuple('ServerType', ["config_type", "port", "replication_port", "debug_port"])
    primary = ServerType(config_type="primary", port=8900, replication_port=8901, debug_port=5005)
    replica = ServerType(config_type="replica", port=8902, replication_port=8903, debug_port=5006)

    def __init__(self, args):
        self._args = args
        self._platypus_base_config = {
            "nodeName": "platypus-{0}",
            "hostName": "localhost",
            "port": "{0}",
            "replicationPort": "{0}",
            "stateDir": f"{args.platypus_data_path}/{{0}}_state",
            "indexDir": f"{args.platypus_data_path}/{{0}}_index",
            "botoCfgPath": args.boto_cfg_file_path,
            "bucketName": args.bucket_name,
            "archiveDirectory": f"{args.platypus_data_path}/{{0}}_archiver",
            "serviceName": f"{args.service_name}",
            "restoreState": False if args.restore_state == "no" else True,
            "restoreFromIncArchiver": "true",
            "backupWithIncArchiver": "true",
            "downloadAsStream": "true"
        }

    def _build_config_for(self, server_type):
        config = self._platypus_base_config.copy()
        for item in ["nodeName", "stateDir", "indexDir", "archiveDirectory"]:
            config[item] = config[item].format(server_type.config_type)
        config["port"] = config["port"].format(server_type.port)
        config["replicationPort"] = config["replicationPort"].format(server_type.replication_port)
        return config

    def _write_server_config_files(self):
        for server_type in [self.primary, self.replica]:
            config = self._build_config_for(server_type)
            with open(f"/user/app/config/{server_type.config_type}.json", "w") as f:
                json.dump(config, f)
            print(json.loads(open(f"/user/app/config/{server_type.config_type}.json", "r").read()))

    @staticmethod
    def _reader(pipe, queue):
        try:
            with pipe:
                for line in iter(pipe.readline, b''):
                    queue.put((pipe, line))
        finally:
            queue.put(None)

    @staticmethod
    def _start_server_process(server_type):
        java_args = f"-Xms4g -Xmx4g -Xss256k -XX:+UseG1GC -XX:+UseCompressedOops " \
                    f"-Xlog:gc:/user/app/log/{server_type.config_type}-gc.log -XX:+HeapDumpOnOutOfMemoryError " \
                    f"-XX:HeapDumpPath=/user/app/log/{server_type.config_type}-heapdump.bin " \
                    f"-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:{server_type.debug_port}"
        os.environ["JAVA_OPTS"] = java_args
        java_server_cmd = "./build/install/nrtsearch/bin/lucene-server"
        java_server_arg = f"/user/app/config/{server_type.config_type}.json"
        return Popen([java_server_cmd, java_server_arg], stdout=PIPE, stderr=PIPE, bufsize=1)

    @staticmethod
    def _fetch_output(processes):
        q = Queue()
        for process in processes:
            Thread(target=ServerProcManager._reader, args=[process.stdout, q]).start()
            Thread(target=ServerProcManager._reader, args=[process.stderr, q]).start()
        for _ in range(4):
            for source, line in iter(q.get, None):
                print("%s: %s" % (source, line))

    def start(self):
        self._write_server_config_files()
        self._fetch_output([self._start_server_process(self.primary),
                            self._start_server_process(self.replica)])


if __name__ == '__main__':
    main()
